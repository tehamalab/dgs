from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify, truncatechars
from django.utils.functional import cached_property


class Goal(models.Model):
    code = models.CharField(_('Goal number'), max_length=10,
                            unique=True)
    name = models.CharField(_('Goal name'), max_length=255)
    description = models.TextField(_('Goal description'), blank=True)
    slug = models.SlugField(_('Slug'))
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


class Indicator(models.Model):
    YES = 'YES'
    NO = 'NO'
    STATS_AVAILABLE_CHOICES = (
        (YES, _('Yes')),
        (NO, _('No')),
    )
    goal = models.ForeignKey(Goal, verbose_name=_('Goal'))
    code = models.CharField(_('Indicator number'), max_length=10,
                            unique=True)
    description = models.TextField(_('Indicator description'),
                                  blank=True)
    target_description = models.TextField(_('Target description'),
                                  blank=True)
    stats_available = models.CharField(
        _('Statistics are availble'), max_length=50, blank=True,
        choices=STATS_AVAILABLE_CHOICES)
    data_source = models.CharField(_('Data source'), max_length=255,
                                   blank=True)
    agency = models.CharField(_('Agency'), max_length=255, blank=True)
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
                                  verbose_name=_('Indicator'))
    code = models.CharField(_('Component number'), max_length=10,
                            unique=True)
    name = models.CharField(_('Component name'), max_length=255)
    description = models.TextField(_('Component description'),
                                  blank=True)
    slug = models.SlugField(_('Slug'))
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
                                  verbose_name=_('Component'))
    year = models.IntegerField(_('Year'))
    value = models.FloatField(_('Value'))
    value_unit = models.CharField(_('Value unit'), blank=True, max_length=50)
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
    def indicator_code(self):
        return self.component.indicator.code
