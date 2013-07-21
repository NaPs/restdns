# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Zone'
        db.create_table(u'restdns_zone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('refresh', self.gf('django.db.models.fields.IntegerField')(default=86400)),
            ('retry', self.gf('django.db.models.fields.IntegerField')(default=7200)),
            ('expire', self.gf('django.db.models.fields.IntegerField')(default=3600000)),
            ('minimum', self.gf('django.db.models.fields.IntegerField')(default=172800)),
            ('serial', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('primary_ns', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'restdns', ['Zone'])

        # Adding model 'Record'
        db.create_table(u'restdns_record', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='5794e672-e5f9-46d6-9d01-24c8c23e8377', unique=True, max_length=36)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restdns.Zone'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('parameters', self.gf('restdns.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'restdns', ['Record'])


    def backwards(self, orm):
        # Deleting model 'Zone'
        db.delete_table(u'restdns_zone')

        # Deleting model 'Record'
        db.delete_table(u'restdns_record')


    models = {
        u'restdns.record': {
            'Meta': {'object_name': 'Record'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'parameters': ('restdns.fields.JSONField', [], {'default': '{}'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'2a4a03a8-caa7-4e4c-a3aa-6f4be7648edf'", 'unique': 'True', 'max_length': '36'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['restdns.Zone']"})
        },
        u'restdns.zone': {
            'Meta': {'object_name': 'Zone'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'expire': ('django.db.models.fields.IntegerField', [], {'default': '3600000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minimum': ('django.db.models.fields.IntegerField', [], {'default': '172800'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'primary_ns': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'refresh': ('django.db.models.fields.IntegerField', [], {'default': '86400'}),
            'retry': ('django.db.models.fields.IntegerField', [], {'default': '7200'}),
            'rname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'serial': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['restdns']