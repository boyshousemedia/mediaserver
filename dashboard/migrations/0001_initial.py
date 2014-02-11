# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServerTime'
        db.create_table(u'dashboard_servertime', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'dashboard', ['ServerTime'])

        # Adding model 'Episode'
        db.create_table(u'dashboard_episode', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('season', self.gf('django.db.models.fields.IntegerField')()),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('overview', self.gf('django.db.models.fields.TextField')()),
            ('air_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('show_id', self.gf('django.db.models.fields.IntegerField')()),
            ('show_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('downloading', self.gf('django.db.models.fields.BooleanField')()),
            ('dl_hash', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'dashboard', ['Episode'])

        # Adding model 'Show'
        db.create_table(u'dashboard_show', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('air_day', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('air_time', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('banner', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('poster', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('download', self.gf('django.db.models.fields.BooleanField')()),
            ('search', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'dashboard', ['Show'])


    def backwards(self, orm):
        # Deleting model 'ServerTime'
        db.delete_table(u'dashboard_servertime')

        # Deleting model 'Episode'
        db.delete_table(u'dashboard_episode')

        # Deleting model 'Show'
        db.delete_table(u'dashboard_show')


    models = {
        u'dashboard.episode': {
            'Meta': {'object_name': 'Episode'},
            'air_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dl_hash': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'downloading': ('django.db.models.fields.BooleanField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'overview': ('django.db.models.fields.TextField', [], {}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {}),
            'show_id': ('django.db.models.fields.IntegerField', [], {}),
            'show_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dashboard.servertime': {
            'Meta': {'object_name': 'ServerTime'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dashboard.show': {
            'Meta': {'object_name': 'Show'},
            'air_day': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'air_time': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'banner': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'download': ('django.db.models.fields.BooleanField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'poster': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'search': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['dashboard']