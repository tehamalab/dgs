import json
from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify, truncatechars
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse
from mptt.models import MPTTModel, TreeForeignKey
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class AreaType(models.Model):
    code = models.CharField(_('Code'), max_length=20, unique=True)
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'),
                                         auto_now=True)
    extras = HStoreField(_('Extras'), blank=True, null=True, default={})

    class Meta:
        verbose_name = _('Area Type')
        verbose_name_plural = _('Area Types')

    def __str__(self):
        return self.name


class Area(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)
    code = models.CharField(_('Area code'), max_length=20, unique=True)
    name = models.CharField(_('Area name'), max_length=255)
    type = models.ForeignKey('goals.AreaType', verbose_name=_('Area type'),
                             related_name='areas', null=True,
                             blank=True)
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
        if self.type:
            self.extras['type_code'] = self.type.code
            self.extras['type_name'] = self.type.name
        super(Area, self).save(*args, **kwargs)

    def get_slug(self):
        if not self.slug:
            slug = slugify(self.name[:50])
            return slug
        return self.slug

    @cached_property
    def api_url(self):
        try:
            return reverse('area-detail', args=[self.pk])
        except:
            # API isn't installed
            # FIXME: Catch a specific exception
            return ''

    @cached_property
    def type_code(self):
        if self.type:
            return self.extras.get('type_code', '') or self.type.code
        return ""

    @cached_property
    def type_name(self):
        if self.type:
            return self.extras.get('type_name', '') or self.type.name
        return ""


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

    def get_slug(self):
        if not self.slug:
            slug = slugify(self.name[:50])
            return slug
        return self.slug

    @cached_property
    def api_url(self):
        try:
            return reverse('plan-detail', args=[self.pk])
        except:
            # API isn't installed
            # FIXME: Catch a specific exception
            return ''

    @cached_property
    def image_url(self):
        if self.image:
            return self.image.url

    @cached_property
    def image_small_url(self):
        if self.image_small:
            return self.image_small.url

    @cached_property
    def image_medium_url(self):
        if self.image_medium:
            return self.image_medium.url

    @cached_property
    def image_large_url(self):
        if self.image_large:
            return self.image_large.url


class Goal(models.Model):
    plan = models.ForeignKey('goals.Plan', verbose_name='plan',
                             related_name='goals')
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
        self.extras['plan_name'] = self.plan.name
        self.extras['plan_code'] = self.plan.code
        super(Goal, self).save(*args, **kwargs)


    def get_slug(self):
        if not self.slug:
            slug = slugify(self.name[:50])
            return slug
        return self.slug

    @cached_property
    def api_url(self):
        try:
            return reverse('goal-detail', args=[self.pk])
        except:
            # API isn't installed
            # FIXME: Catch a specific exception
            return ''

    @cached_property
    def image_url(self):
        if self.image:
            return self.image.url

    @cached_property
    def image_small_url(self):
        if self.image_small:
            return self.image_small.url

    @cached_property
    def image_medium_url(self):
        if self.image_medium:
            return self.image_medium.url

    @cached_property
    def image_large_url(self):
        if self.image_large:
            return self.image_large.url

    @cached_property
    def plan_name(self):
        return self.extras.get('plan_name', '') or self.plan.name

    @cached_property
    def plan_code(self):
        return self.extras.get('plan_code', '') or self.plan.code


class Target(models.Model):
    goal = models.ForeignKey(Goal, verbose_name=_('Goal'),
                             related_name='targets')
    code = models.CharField(_('Target number'), max_length=10,
                            unique=True)
    name = models.CharField(_('Target'), max_length=255)
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
    slug = models.SlugField(_('Slug'), blank=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        self.extras['goal_code'] = self.goal.code
        self.extras['goal_name'] = self.goal.name
        self.extras['plan_id'] = self.plan.id
        self.extras['plan_code'] = self.plan.code
        self.extras['plan_name'] = self.plan.name
        super(Target, self).save(*args, **kwargs)

    def get_slug(self):
        if not self.slug:
            slug = slugify(self.name[:50])
            return slug
        return self.slug

    @cached_property
    def api_url(self):
        try:
            return reverse('target-detail', args=[self.pk])
        except:
            # API isn't installed
            # FIXME: Catch a specific exception
            return ''

    @cached_property
    def image_url(self):
        if self.image:
            return self.image.url

    @cached_property
    def image_small_url(self):
        if self.image_small:
            return self.image_small.url

    @cached_property
    def image_medium_url(self):
        if self.image_medium:
            return self.image_medium.url

    @cached_property
    def image_large_url(self):
        if self.image_large:
            return self.image_large.url

    @cached_property
    def goal_code(self):
        return self.extras.get('goal_code', '') or self.goal.code

    @cached_property
    def goal_name(self):
        return self.extras.get('goal_name', '') or self.goal.name

    @cached_property
    def plan(self):
        return self.goal.plan

    @cached_property
    def plan_id(self):
        return int(self.extras.get('plan_id', '0')) or self.goal.plan_id

    @cached_property
    def plan_code(self):
        return self.extras.get('plan_code', '') or self.goal.plan_code

    @cached_property
    def plan_name(self):
        return self.extras.get('plan_name', '') or self.goal.plan_name


class Indicator(models.Model):
    target = models.ForeignKey(Target, verbose_name=_('Target'),
                               related_name='indicators')
    name = models.CharField(_('Indicator'), max_length=255)
    code = models.CharField(_('Indicator number'), max_length=10,
                            unique=True)
    description = models.TextField(_('Indicator description'),
                                  blank=True)
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
    slug = models.SlugField(_('Slug'), blank=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        self.extras['target_code'] = self.target.code
        self.extras['target_name'] = self.target.name
        self.extras['goal_id'] = self.goal.id
        self.extras['goal_code'] = self.goal.code
        self.extras['goal_name'] = self.goal.name
        self.extras['plan_id'] = self.plan.id
        self.extras['plan_code'] = self.plan.code
        self.extras['plan_name'] = self.plan.name
        super(Indicator, self).save(*args, **kwargs)

    def get_slug(self):
        if not self.slug:
            slug = slugify(self.name[:50])
            return slug
        return self.slug

    @cached_property
    def api_url(self):
        try:
            return reverse('indicator-detail', args=[self.pk])
        except:
            # API isn't installed
            # FIXME: Catch a specific exception
            return ''

    @cached_property
    def image_url(self):
        if self.image:
            return self.image.url

    @cached_property
    def image_small_url(self):
        if self.image_small:
            return self.image_small.url

    @cached_property
    def image_medium_url(self):
        if self.image_medium:
            return self.image_medium.url

    @cached_property
    def image_large_url(self):
        if self.image_large:
            return self.image_large.url

    @cached_property
    def target_code(self):
        return self.extras.get('target_code', '') or self.target.code

    @cached_property
    def target_name(self):
        return self.extras.get('target_name', '') or self.target.name

    @cached_property
    def goal(self):
        return self.target.goal

    @cached_property
    def goal_id(self):
        return int(self.extras.get('goal_id', '0')) or self.goal.id

    @cached_property
    def goal_code(self):
        return self.extras.get('goal_code', '') or self.goal.code

    @cached_property
    def goal_name(self):
        return self.extras.get('goal_name', '') or self.goal.name

    @cached_property
    def plan(self):
        return self.target.goal.plan

    @cached_property
    def plan_id(self):
        return int(self.extras.get('plan_id', '0')) or self.goal.plan_id

    @cached_property
    def plan_code(self):
        return self.extras.get('plan_code', '') or self.goal.plan_code

    @cached_property
    def plan_name(self):
        return self.extras.get('plan_name', '') or self.goal.plan_name


class Component(models.Model):
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
    indicators = models.ManyToManyField('goals.Indicator',
                                        verbose_name=_('Indicators'),
                                        related_name='components')
    code = models.CharField(_('Component number'), max_length=10,
                            blank=True)
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
    stats_available = models.CharField(
        _('Statistics availble'), max_length=50, blank=True,
        choices=STATS_AVAILABLE_CHOICES, default=UNKNOWN)
    data_source = models.CharField(_('Data source'), max_length=255,
                                   blank=True)
    agency = models.CharField(_('Agency'), max_length=255, blank=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        indctrs = self.indicators\
            .prefetch_related('target', 'target__goal', 'target__goal__plan')
        self.extras['indicators_codes'] = json.dumps([i.code for i in indctrs])
        self.extras['indicators_names'] = json.dumps([i.name for i in indctrs])
        self.extras['targets_ids'] = json.dumps([i.target.id for i in indctrs])
        self.extras['targets_codes'] = json.dumps([i.target.code for i in indctrs])
        self.extras['targets_names'] = json.dumps([i.target.name for i in indctrs])
        self.extras['goals_ids'] = json.dumps([i.target.goal.id for i in indctrs])
        self.extras['goals_codes'] = json.dumps([i.target.goal.code for i in indctrs])
        self.extras['goals_names'] = json.dumps([i.target.goal.name for i in indctrs])
        self.extras['plans_ids'] = json.dumps([i.target.goal.plan.id for i in indctrs])
        self.extras['plans_codes'] = json.dumps([i.target.goal.plan.code for i in indctrs])
        self.extras['plans_names'] = json.dumps([i.target.goal.plan.name for i in indctrs])
        super(Component, self).save(*args, **kwargs)

    def get_slug(self):
        if not self.slug:
            slug = slugify(self.name[:50])
            return slug
        return self.slug

    @cached_property
    def api_url(self):
        try:
            return reverse('component-detail', args=[self.pk])
        except:
            # API isn't installed
            # FIXME: Catch a specific exception
            return ''

    @cached_property
    def image_url(self):
        if self.image:
            return self.image.url

    @cached_property
    def image_small_url(self):
        if self.image_small:
            return self.image_small.url

    @cached_property
    def image_medium_url(self):
        if self.image_medium:
            return self.image_medium.url

    @cached_property
    def image_large_url(self):
        if self.image_large:
            return self.image_large.url

    @cached_property
    def indicators_codes(self):
        return json.loads(self.extras.get('indicators_codes', '[]')) \
            or list(self.indicators.values_list('code', flat=True))

    @cached_property
    def indicators_names(self):
        return json.loads(self.extras.get('indicators_names', '[]')) \
            or list(self.indicators.values_list('name', flat=True))

    @cached_property
    def targets_ids(self):
        return json.loads(self.extras.get('targets_ids', '[]'))

    @cached_property
    def targets_codes(self):
        return json.loads(self.extras.get('targets_codes', '[]'))

    @cached_property
    def targets_names(self):
        return json.loads(self.extras.get('targets_names', '[]'))

    @cached_property
    def goals_ids(self):
        return json.loads(self.extras.get('goals_ids', '[]'))

    @cached_property
    def goals_codes(self):
        return json.loads(self.extras.get('goals_codes', '[]'))

    @cached_property
    def goals_names(self):
        return json.loads(self.extras.get('goals_names', '[]'))

    @cached_property
    def plans_ids(self):
        return json.loads(self.extras.get('plans_ids', '[]'))

    @cached_property
    def plans_codes(self):
        return json.loads(self.extras.get('plans_codes', '[]'))

    @cached_property
    def plans_names(self):
        return json.loads(self.extras.get('plans_names', '[]'))


class Progress(models.Model):
    component = models.ForeignKey(Component,
                                  verbose_name=_('Component'),
                                  related_name='progress')
    area = models.ForeignKey(Area, verbose_name=_('Area'),
                             related_name='progress')
    groups = ArrayField(
        models.CharField(max_length=50, blank=True), null=True,
        blank=True, verbose_name=_('Groups'), default=[])
    year = models.IntegerField(_('Year'))
    value = models.FloatField(_('Value'))
    remarks = models.TextField(_('Remarks'), blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'),
                                         auto_now=True)
    extras = HStoreField(_('Extras'), blank=True, null=True, default={})

    class Meta:
        verbose_name = _('Progress')
        verbose_name_plural = _('Progress')

    def __str__(self):
        return '%d:%d' %(self.year, self.value)

    def save(self, *args, **kwargs):
        self.extras['area_code'] = self.area.code
        self.extras['area_name'] = self.area.name
        self.extras['component_code'] = self.component.code
        self.extras['component_name'] = self.component.name
        self.extras['value_unit'] = self.component.value_unit
        super(Progress, self).save(*args, **kwargs)

    @cached_property
    def api_url(self):
        try:
            return reverse('progress-detail', args=[self.pk])
        except:
            # API isn't installed
            # FIXME: Catch a specific exception
            return ''

    @cached_property
    def component_code(self):
        return self.extras.get('component_code', '')\
            or self.component.code

    @cached_property
    def component_name(self):
        return self.extras.get('component_name', '')\
            or self.component.name

    @cached_property
    def area_code(self):
        return self.extras.get('area_code', '') or self.area.code

    @cached_property
    def area_name(self):
        return self.extras.get('area_name', '') or self.area.name

    @cached_property
    def value_unit(self):
        return self.extras.get('value_unit', '')
