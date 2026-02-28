from django.db import models


class Crop(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Field(models.Model):
    class FieldType(models.TextChoices):
        GREENHOUSE = 'greenhouse', 'Greenhouse'
        OPEN = 'open', 'Open'

    class AreaUnit(models.TextChoices):
        SOTKA = 'sotka', 'Sotka'
        HA = 'ha', 'Ha'

    name = models.CharField(max_length=200, unique=True)
    field_type = models.CharField(max_length=20, choices=FieldType.choices)
    area = models.DecimalField(max_digits=8, decimal_places=2)
    area_unit = models.CharField(max_length=20, choices=AreaUnit.choices, default=AreaUnit.SOTKA)

    def __str__(self):
        return self.name


class Category(models.Model):
    class CategoryGroup(models.TextChoices):
        PROTECTION = 'protection', 'Protection'
        FERTILIZER = 'fertilizer', 'Fertilizer'

    name = models.CharField(max_length=120)
    group = models.CharField(max_length=20, choices=CategoryGroup.choices)

    def __str__(self):
        return f'{self.name} ({self.get_group_display()})'


class Product(models.Model):
    name = models.CharField(max_length=160)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    active_ingredient = models.CharField(max_length=200, blank=True)
    formulation = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Issue(models.Model):
    class IssueKind(models.TextChoices):
        DISEASE = 'disease', 'Disease'
        PEST = 'pest', 'Pest'
        DEFICIENCY = 'deficiency', 'Deficiency'

    name = models.CharField(max_length=160)
    kind = models.CharField(max_length=20, choices=IssueKind.choices)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='issues')
    short_description = models.CharField(max_length=300, blank=True)
    symptoms = models.TextField(blank=True)
    image = models.ImageField(upload_to='issues/', blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.crop})'


class IssueRecommendation(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='recommendations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='issue_recommendations')
    rank = models.PositiveIntegerField(default=1)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ('issue', 'product')
        ordering = ['rank', 'id']


class DosageRule(models.Model):
    class Dose10LUnit(models.TextChoices):
        ML_10L = 'ml_10l', 'ml/10L'
        G_10L = 'g_10l', 'g/10L'

    class DoseHaUnit(models.TextChoices):
        L_HA = 'l_ha', 'L/ha'
        KG_HA = 'kg_ha', 'kg/ha'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='dosage_rules')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='dosage_rules')
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True, blank=True, related_name='dosage_rules')
    dose_10l_value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dose_10l_unit = models.CharField(max_length=20, choices=Dose10LUnit.choices, blank=True)
    dose_per_ha_value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dose_per_ha_unit = models.CharField(max_length=20, choices=DoseHaUnit.choices, blank=True)
    interval_days = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)


class IrrigationLog(models.Model):
    date_time = models.DateTimeField()
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='irrigation_logs')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='irrigation_logs')
    water_liters = models.DecimalField(max_digits=10, decimal_places=2)
    duration_min = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_time']


class SprayLog(models.Model):
    date_time = models.DateTimeField()
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='spray_logs')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='spray_logs')
    target_issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True, blank=True, related_name='spray_logs')
    water_rate_note = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_time']


class SprayMixItem(models.Model):
    spray = models.ForeignKey(SprayLog, on_delete=models.CASCADE, related_name='mix_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='spray_mix_items')
    dose_text = models.CharField(max_length=120)
    notes = models.TextField(blank=True)
