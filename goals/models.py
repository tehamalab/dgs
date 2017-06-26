from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify, truncatechars
from django.utils.functional import cached_property
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class Area(models.Model):
    code = models.CharField(_('Area code'), max_length=10, unique=True)
    name = models.CharField(_('Area name'), max_length=255)
    type = models.CharField(_('Area type'), max_length=255)
    description = models.TextField(_('Area description'), blank=True)
    image = models.ImageField(_('Image'),
                              upload_to='goals/areas/images',
                              blank=True, null=True)
    image_small = ImageSpecField(source='image',
                                 processors=[ResizeToFit(100, 100)],
                                 format='PNG',
                                 options={'quality': 90})
    image_medium = ImageSpecField(source='image',
                                  processors=[ResizeToFit(250, 250)],
                                  format='PNG',
                                  options={'quality': 90})
    image_large = ImageSpecField(source='image',
                                 processors=[ResizeToFit(700)],
                                 options={'quality': 80})
    slug = models.SlugField(_('Slug'), blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'),
                                         auto_now=True)
    extras = HStoreField(_('Extras'), blank=True, null=True, default={})

    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        super(Area, self).save(*args, **kwargs)

    def get_slug(self):
        if not self.slug:
            slug = slugify(self.name[:50])
            return slug
        return self.slug


class Plan(models.Model):
    code = models.CharField(_('code'), max_length=10,
                            unique=True)
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    image = models.ImageField(_('Image'),
                              upload_to='goals/goals/images',
                              blank=True, null=True)
    image_small = ImageSpecField(source='image',
                                 processors=[ResizeToFit(100, 100)],
                                 format='PNG',
                                 options={'quality': 90})
    image_medium = ImageSpecField(source='image',
                                  processors=[ResizeToFit(250, 250)],
                                  format='PNG',
                                  options={'quality': 90})
    image_large = ImageSpecField(source='image',
                                 processors=[ResizeToFit(700)],
                                 options={'quality': 80})
    slug = models.SlugField(_('Slug'), blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'),
                                         auto_now=True)
    extras = HStoreField(_('Extras'), blank=True, null=True, default={})

    class Meta:
        verbose_name = _('Plan')
        verbose_name_plural = _('Plans')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        super(Plan, self).save(*args, **kwargs)


class Goal(models.Model):
    plan = models.ForeignKey('goals.Plan', verbose_name='plan',
                             related_name='goals', blank=True,
                             null=True)
    code = models.CharField(_('Goal number'), max_length=10,
                            unique=True)
    name = models.CharField(_('Goal name'), max_length=255)
    description = models.TextField(_('Goal description'), blank=True)
    image = models.ImageField(_('Image'),
                              upload_to='goals/goals/images',
                              blank=True, null=True)
    image_small = ImageSpecField(source='image',
                                 processors=[ResizeToFit(100, 100)],
                                 format='PNG',
                                 options={'quality': 90})
    image_medium = ImageSpecField(source='image',
                                  processors=[ResizeToFit(250, 250)],
                                  format='PNG',
                                  options={'quality': 90})
    image_large = ImageSpecField(source='image',
                                 processors=[ResizeToFit(700)],
                                 options={'quality': 80})
    slug = models.SlugField(_('Slug'), blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'),
                                         auto_now=True)
    extras = HStoreField(_('Extras'), blank=True, null=True, default={})

    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        super(Goal, self).save(*args, **kwargs)

    def get_slug(self):
        if not self.slug:
            slug = slugify(self.name[:50])
            return slug
        return self.slug


class Target(models.Model):
    goal = models.ForeignKey(Goal, verbose_name=_('Goal'),
                             related_name='targets')
    code = models.CharField(_('Target number'), max_length=10,
                            unique=True)
    description = models.TextField(_('Target description'),
                                  blank=True)
    image = models.ImageField(_('Image'),
                              upload_to='goals/targets/images',
                              blank=True, null=True)
    image_small = ImageSpecField(source='image',
                                 processors=[ResizeToFit(100, 100)],
                                 format='PNG',
                                 options={'quality': 90})
    image_medium = ImageSpecField(source='image',
                                  processors=[ResizeToFit(250, 250)],
                                  format='PNG',
                                  options={'quality': 90})
    image_large = ImageSpecField(source='image',
                                 processors=[ResizeToFit(700)],
                                 options={'quality': 80})
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'),
                                         auto_now=True)
    extras = HStoreField(_('Extras'), blank=True, null=True, default={})

    class Meta:
        verbose_name = _('Target')
        verbose_name_plural = _('Targets')

    def __str__(self):
        return '%s : %s' \
            %(self.code, truncatechars(self.description, 50))


class Indicator(models.Model):
    YES = 'YES'
    NO = 'NO'
    PARTIALLY = 'PARTIALLY'
    UNKNOWN = 'UNKNOWN'
    STATS_AVAILABLE_CHOICES = (
        (YES, _('Yes')),
        (NO, _('No')),
        (PARTIALLY, _('Partially')),
        (UNKNOWN, _('Unknown')),
    )
    target = models.ForeignKey(Target, verbose_name=_('Target'),
                               related_name='indicators')
    code = models.CharField(_('Indicator number'), max_length=10,
                            unique=True)
    description = models.TextField(_('Indicator description'),
                                  blank=True)
    stats_available = models.CharField(
        _('Statistics availble'), max_length=50, blank=True,
        choices=STATS_AVAILABLE_CHOICES, default=UNKNOWN)
    data_source = models.CharField(_('Data source'), max_length=255,
                                   blank=True)
    agency = models.CharField(_('Agency'), max_length=255, blank=True)
    image = models.ImageField(_('Image'),
                              upload_to='goals/indicators/images',
                              blank=True, null=True)
    image_small = ImageSpecField(source='image',
                                 processors=[ResizeToFit(100, 100)],
                                 format='PNG',
                                 options={'quality': 90})
    image_medium = ImageSpecField(source='image',
                                  processors=[ResizeToFit(250, 250)],
                                  format='PNG',
                                  options={'quality': 90})
    image_large = ImageSpecField(source='image',
                                 processors=[ResizeToFit(700)],
                                 options={'quality': 80})
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'),
                                         auto_now=True)
    extras = HStoreField(_('Extras'), blank=True, null=True, default={})

    class Meta:
        verbose_name = _('Indicator')
        verbose_name_plural = _('Indicators')

    def __str__(self):
        return '%s : %s' \
            %(self.code, truncatechars(self.description, 50))


class Component(models.Model):
    indicator = models.ForeignKey(Indicator,
                                  verbose_name=_('Indicator'),
                                  related_name='components')
    code = models.CharField(_('Component number'), max_length=10,
                            unique=True)
    name = models.CharField(_('Component name'), max_length=255)
    description = models.TextField(_('Component description'),
                                  blank=True)
    image = models.ImageField(_('Image'),
                              upload_to='goals/components/images',
                              blank=True, null=True)
    image_small = ImageSpecField(source='image',
                                 processors=[ResizeToFit(100, 100)],
                                 format='PNG',
                                 options={'quality': 90})
    image_medium = ImageSpecField(source='image',
                                  processors=[ResizeToFit(250, 250)],
                                  format='PNG',
                                  options={'quality': 90})
    image_large = ImageSpecField(source='image',
                                 processors=[ResizeToFit(700)],
                                 options={'quality': 80})
    target_value = models.FloatField(_('Target value'), blank=True,
                                     null=True)
    value_unit = models.CharField(_('Value unit'), blank=True,
                                  max_length=50)
    slug = models.SlugField(_('Slug'), blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'),
                                         auto_now=True)
    extras = HStoreField(_('Extras'), blank=True, null=True, default={})

    class Meta:
        verbose_name = _('Component')
        verbose_name_plural = _('Components')

    def __str__(self):
        return self.name


class Progress(models.Model):
    component = models.ForeignKey(Component,
                                  verbose_name=_('Component'),
                                  related_name='progress')
    area = models.ForeignKey(Area, null=True, blank=True,
                             verbose_name=_('Area'),
                             related_name='progress')
    year = models.IntegerField(_('Year'))
    value = models.FloatField(_('Value'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'),
                                         auto_now=True)
    extras = HStoreField(_('Extras'), blank=True, null=True, default={})

    class Meta:
        verbose_name = _('Progress')
        verbose_name_plural = _('Progress')

    def __str__(self):
        return '%d:%d' %(self.year, self.value)

    @cached_property
    def component_code(self):
        return self.component.code

    @cached_property
    def component_name(self):
        return self.component.name

    @cached_property
    def value_unit(self):
        return self.component.value_unit

    @cached_property
    def indicator_code(self):
        return self.component.indicator.code
