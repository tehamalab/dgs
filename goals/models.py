import json
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import HStoreField, ArrayField
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify, truncatechars
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse
from mptt.models import MPTTModel, TreeForeignKey
from mptt.signals import node_moved
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


def area_type_topo_path(instance, filename):
    return 'topojson/areatype/{0}/{1}'.format(instance.code, filename)


class AreaType(models.Model):
    code = models.CharField(_('Code'), max_length=20, unique=True)
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    topojson = models.FileField(_('TopoJSON'), blank=True, null=True,
                                upload_to=area_type_topo_path)
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
    type = models.ForeignKey('goals.AreaType',
                             verbose_name=_('Area type'),
                             related_name='areas')
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
    caption = models.TextField(_('Caption'), blank=True)
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


class Theme(models.Model):
    plans = models.ManyToManyField('goals.Plan', verbose_name='Plans',
                                   related_name='themes')
    name = models.CharField(_('Theme name'), max_length=255)
    code = models.CharField(_('Theme number'), max_length=10)
    description = models.TextField(_('Theme description'), blank=True)
    image = models.ImageField(_('Image'),
                              upload_to='goals/themes/images',
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
        verbose_name = _('Theme')
        verbose_name_plural = _('Themes')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        super(Theme, self).save(*args, **kwargs)

    @cached_property
    def plans_ids(self):
        return json.loads(self.extras.get('plans_ids', '[]'))

    @cached_property
    def plans_codes(self):
        return json.loads(self.extras.get('plans_codes', '[]'))

    @cached_property
    def plans_codes_str(self):
        return ', '.join(json.loads(self.extras.get('plans_codes', '[]')))

    @cached_property
    def plans_names(self):
        return json.loads(self.extras.get('plans_names', '[]'))

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

    @cached_property
    def api_url(self):
        try:
            return reverse('theme-detail', args=[self.pk])
        except:
            # API isn't installed
            # FIXME: Catch a specific exception
            return ''


class SectorType(models.Model):
    code = models.CharField(_('Code'), max_length=20, unique=True)
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'),
                                         auto_now=True)
    extras = HStoreField(_('Extras'), blank=True, null=True, default={})

    class Meta:
        verbose_name = _('Sector Type')
        verbose_name_plural = _('Sector Types')

    def __str__(self):
        return self.name



class Sector(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)
    name = models.CharField(_('Sector name'), max_length=255)
    code = models.CharField(_('Sector code'), max_length=20)
    type = models.ForeignKey('goals.SectorType',
                             verbose_name=_('Sector type'),
                             related_name='sextors')
    description = models.TextField(_('Sector description'), blank=True)
    image = models.ImageField(_('Image'),
                              upload_to='goals/sectors/images',
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
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        if self.type:
            self.extras['type_code'] = self.type.code
            self.extras['type_name'] = self.type.name
        super(Sector, self).save(*args, **kwargs)

    def get_slug(self):
        if not self.slug:
            slug = slugify(self.name[:50])
            return slug
        return self.slug

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
    def type_code(self):
        return self.extras.get('type_code', '') or self.type.code

    @cached_property
    def type_name(self):
        return self.extras.get('type_name', '') or self.type.name

    @cached_property
    def ancestors_ids(self):
        return json.loads(self.extras.get('ancestors_ids', '[]'))\
            or [ancestor.id for ancestor in self.get_ancestors()]

    @cached_property
    def ancestors_codes(self):
        return json.loads(self.extras.get('ancestors_codes', '[]'))\
            or [ancestor.code for ancestor in self.get_ancestors()]

    @cached_property
    def ancestors_names(self):
        return json.loads(self.extras.get('ancestors_names', '[]'))\
            or [ancestor.name for ancestor in self.get_ancestors()]

    @cached_property
    def api_url(self):
        try:
            return reverse('sector-detail', args=[self.pk])
        except:
            # API isn't installed
            # FIXME: Catch a specific exception
            return ''


class Goal(models.Model):
    plan = models.ForeignKey('goals.Plan', verbose_name='plan',
                             related_name='goals')
    code = models.CharField(_('Goal number'), max_length=10)
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
        unique_together = ['code', 'plan']

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
    code = models.CharField(_('Target number'), max_length=10)
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
        unique_together = ['code', 'goal']

    def __str__(self):
        return '%s %s : %s' %(self.plan_code, self.code, truncatechars(self.description, 50))

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
    theme = models.ForeignKey('goals.Theme', verbose_name=_('Theme'),
                              related_name='indicators', null=True, blank=True)
    sector = models.ForeignKey('goals.Sector', verbose_name=_('Sector'),
                              related_name='indicators', null=True, blank=True)
    target = models.ForeignKey(Target, verbose_name=_('Target'),
                               related_name='indicators', null=True, blank=True)
    name = models.CharField(_('Indicator'), max_length=255)
    code = models.CharField(_('Indicator number'), max_length=10)
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
        unique_together = ['code', 'target', 'sector', 'theme']

    def __str__(self):
        return '%s %s : %s' \
            %(self.plan_code, self.code, truncatechars(self.description, 50))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        if self.theme:
            self.extras['theme_code'] = self.theme.code
            self.extras['theme_name'] = self.theme.name
        if self.sector:
            self.extras['sector_code'] = self.sector.code
            self.extras['sector_name'] = self.sector.name
            self.extras['sectors_ids'] = json.dumps([self.sector_id] + self.sector.ancestors_ids)
            self.extras['sectors_codes'] = json.dumps([self.sector.code] + self.sector.ancestors_codes)
            self.extras['sectors_names'] = json.dumps([self.sector.name] + self.sector.ancestors_names)
            self.extras['sector_type_code'] = self.sector.type.code
            self.extras['sector_type_name'] = self.sector.type.name
            self.extras['root_sector_id'] = self.sector.get_root().id
            self.extras['root_sector_code'] = self.sector.get_root().code
            self.extras['root_sector_name'] = self.sector.get_root().name
        if self.target:
            self.extras['target_code'] = self.target.code
            self.extras['target_name'] = self.target.name
        if self.goal:
            self.extras['goal_id'] = self.goal.id
            self.extras['goal_code'] = self.goal.code
            self.extras['goal_name'] = self.goal.name
        if self.plan:
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
    def theme_code(self):
        return self.extras.get('theme_code', '')

    @cached_property
    def theme_name(self):
        return self.extras.get('theme_name', '')

    @cached_property
    def sectors_ids(self):
        if self.sector:
            return json.loads(self.extras.get('sectors_ids', '[]'))
        return []

    @cached_property
    def sectors_names(self):
        if self.sector:
            return json.loads(self.extras.get('sectors_names', '[]'))
        return []

    @cached_property
    def sectors_codes(self):
        if self.sector:
            return json.loads(self.extras.get('sectors_codes', '[]'))
        return []

    @cached_property
    def sector_type_code(self):
        return self.extras.get('sector_type_code', '')

    @cached_property
    def sector_type_name(self):
        return self.extras.get('sector_type_name', '')

    @cached_property
    def sector_code(self):
        return self.extras.get('sector_code', '')

    @cached_property
    def sector_name(self):
        return self.extras.get('sector_name', '')

    @cached_property
    def root_sector_id(self):
        return int(self.extras.get('root_sector_id', '0')) or None

    @cached_property
    def root_sector_code(self):
        return self.extras.get('root_sector_code', '')

    @cached_property
    def root_sector_name(self):
        return self.extras.get('root_sector_name', '')

    @cached_property
    def target_code(self):
        return self.extras.get('target_code', '')

    @cached_property
    def target_name(self):
        return self.extras.get('target_name', '')

    @cached_property
    def goal(self):
        if self.target:
            return self.target.goal
        return None

    @cached_property
    def goal_id(self):
        return int(self.extras.get('goal_id', '0')) or None

    @cached_property
    def goal_code(self):
        return self.extras.get('goal_code', '')

    @cached_property
    def goal_name(self):
        return self.extras.get('goal_name', '')

    @cached_property
    def plan(self):
        if self.target:
            return self.target.goal.plan
        return None

    @cached_property
    def plan_id(self):
        return int(self.extras.get('plan_id', '0')) or None

    @cached_property
    def plan_code(self):
        return self.extras.get('plan_code', '')


    @cached_property
    def plan_name(self):
        return self.extras.get('plan_name', '')

    def get_progress_count(self):
        return Progress.objects.filter(component__indicators=self.id).count()

    def get_progress_preview(self):
        return Progress.objects.filter(component__indicators=self.id)\
            .order_by('component__indicators', '-year')\
            .distinct('component__indicators')


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

    def get_progress_count(self):
        return Progress.objects.filter(component=self.id).count()


class Progress(models.Model):
    component = models.ForeignKey(Component,
                                  verbose_name=_('Component'),
                                  related_name='progress')
    area = models.ForeignKey(Area, verbose_name=_('Area'),
                             related_name='progress')
    groups = ArrayField(
        models.CharField(max_length=50, blank=True), null=True,
        blank=True, verbose_name=_('Groups'), default=[])
    year = models.PositiveIntegerField(_('Year'))
    fiscal_year = models.CharField(_('Fiscal year'), max_length=9,
                                   blank=True)
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
        self.extras['area_type_id'] = self.area.type_id
        self.extras['area_type_code'] = self.area.type_code
        self.extras['area_type_name'] = self.area.type_name
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
    def area_type_id(self):
        return int(self.extras.get('area_type_id', 0))\
            or self.area.type_id

    @cached_property
    def area_type_code(self):
        return self.extras.get('area_type_code', '')\
            or self.area.type_code

    @cached_property
    def area_type_name(self):
        return self.extras.get('area_type_name', '')\
            or self.area.type_name

    @cached_property
    def value_unit(self):
        return self.extras.get('value_unit', '')


@receiver(m2m_changed, sender=Theme.plans.through)
def theme_plans_changed(sender, instance, action, **kwargs):
    if action == 'post_add':
        plans = instance.plans.all()
        instance.extras['plans_ids'] = json.dumps([i.id for i in plans])
        instance.extras['plans_names'] = json.dumps([i.name for i in plans])
        instance.extras['plans_codes'] = json.dumps([i.code for i in plans])
        Theme.objects.filter(id=instance.id).update(extras=instance.extras)


@receiver(m2m_changed, sender=Component.indicators.through)
def component_indicators_changed(sender, instance, action, **kwargs):
    if action == 'post_add':
        indctrs = instance.indicators\
            .prefetch_related('target', 'target__goal', 'target__goal__plan')
        instance.extras['indicators_codes'] = json.dumps([i.code for i in indctrs])
        instance.extras['indicators_names'] = json.dumps([i.name for i in indctrs])
        instance.extras['targets_ids'] = json.dumps([i.target.id for i in indctrs])
        instance.extras['targets_codes'] = json.dumps([i.target.code for i in indctrs])
        instance.extras['targets_names'] = json.dumps([i.target.name for i in indctrs])
        instance.extras['goals_ids'] = json.dumps([i.target.goal.id for i in indctrs])
        instance.extras['goals_codes'] = json.dumps([i.target.goal.code for i in indctrs])
        instance.extras['goals_names'] = json.dumps([i.target.goal.name for i in indctrs])
        instance.extras['plans_ids'] = json.dumps([i.target.goal.plan.id for i in indctrs])
        instance.extras['plans_codes'] = json.dumps([i.target.goal.plan.code for i in indctrs])
        instance.extras['plans_names'] = json.dumps([i.target.goal.plan.name for i in indctrs])
        Component.objects.filter(id=instance.id).update(extras=instance.extras)


@receiver(node_moved, sender=Sector)
def sector_node_moved(sender, instance, **kwargs):
    instance.extras['ancestors_ids'] = json.dumps(
        [ancestor.id for ancestor in instance.get_ancestors()])
    instance.extras['ancestors_codes'] = json.dumps(
        [ancestor.code for ancestor in instance.get_ancestors()])
    instance.extras['ancestors_names'] = json.dumps(
        [ancestor.name for ancestor in instance.get_ancestors()])
    Sector.objects.filter(id=instance.id).update(extras=instance.extras)
