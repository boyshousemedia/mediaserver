# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Disk'
        db.create_table(u'disk_disk', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('capacity_terabytes', self.gf('django.db.models.fields.FloatField')()),
            ('available_terabytes', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'disk', ['Disk'])


    def backwards(self, orm):
        # Deleting model 'Disk'
        db.delete_table(u'disk_disk')


    models = {
        u'disk.disk': {
            'Meta': {'object_name': 'Disk'},
            'available_terabytes': ('django.db.models.fields.FloatField', [], {}),
            'capacity_terabytes': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['disk']