# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cowboy.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import src.generated.shared_pb2 as shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x63owboy.proto\x1a\x0cshared.proto\"\x1e\n\x08Response\x12\x12\n\nstatusCode\x18\x01 \x01(\t\"6\n\x06\x43owboy\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06health\x18\x02 \x01(\x05\x12\x0e\n\x06\x64\x61mage\x18\x03 \x01(\x05\"\'\n\x07Shooter\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x61mage\x18\x02 \x01(\x05\":\n\x0cTargetCowboy\x12\x16\n\x0eserviceAddress\x18\x01 \x01(\t\x12\x12\n\ncowboyName\x18\x02 \x01(\t\".\n\rTargetCowboys\x12\x1d\n\x06target\x18\x01 \x03(\x0b\x32\r.TargetCowboy2\xc9\x01\n\rCowboyService\x12\x1d\n\tgetCowboy\x12\x05.Void\x1a\x07.Cowboy\"\x00\x12!\n\tsetCowboy\x12\x07.Cowboy\x1a\t.Response\"\x00\x12/\n\x10setTargetCowboys\x12\x0e.TargetCowboys\x1a\t.Response\"\x00\x12 \n\ngiveDamage\x12\x05.Void\x1a\t.Response\"\x00\x12#\n\ntakeDamage\x12\x08.Shooter\x1a\t.Response\"\x00\x62\x06proto3')



_RESPONSE = DESCRIPTOR.message_types_by_name['Response']
_COWBOY = DESCRIPTOR.message_types_by_name['Cowboy']
_SHOOTER = DESCRIPTOR.message_types_by_name['Shooter']
_TARGETCOWBOY = DESCRIPTOR.message_types_by_name['TargetCowboy']
_TARGETCOWBOYS = DESCRIPTOR.message_types_by_name['TargetCowboys']
Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'cowboy_pb2'
  # @@protoc_insertion_point(class_scope:Response)
  })
_sym_db.RegisterMessage(Response)

Cowboy = _reflection.GeneratedProtocolMessageType('Cowboy', (_message.Message,), {
  'DESCRIPTOR' : _COWBOY,
  '__module__' : 'cowboy_pb2'
  # @@protoc_insertion_point(class_scope:Cowboy)
  })
_sym_db.RegisterMessage(Cowboy)

Shooter = _reflection.GeneratedProtocolMessageType('Shooter', (_message.Message,), {
  'DESCRIPTOR' : _SHOOTER,
  '__module__' : 'cowboy_pb2'
  # @@protoc_insertion_point(class_scope:Shooter)
  })
_sym_db.RegisterMessage(Shooter)

TargetCowboy = _reflection.GeneratedProtocolMessageType('TargetCowboy', (_message.Message,), {
  'DESCRIPTOR' : _TARGETCOWBOY,
  '__module__' : 'cowboy_pb2'
  # @@protoc_insertion_point(class_scope:TargetCowboy)
  })
_sym_db.RegisterMessage(TargetCowboy)

TargetCowboys = _reflection.GeneratedProtocolMessageType('TargetCowboys', (_message.Message,), {
  'DESCRIPTOR' : _TARGETCOWBOYS,
  '__module__' : 'cowboy_pb2'
  # @@protoc_insertion_point(class_scope:TargetCowboys)
  })
_sym_db.RegisterMessage(TargetCowboys)

_COWBOYSERVICE = DESCRIPTOR.services_by_name['CowboyService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RESPONSE._serialized_start=30
  _RESPONSE._serialized_end=60
  _COWBOY._serialized_start=62
  _COWBOY._serialized_end=116
  _SHOOTER._serialized_start=118
  _SHOOTER._serialized_end=157
  _TARGETCOWBOY._serialized_start=159
  _TARGETCOWBOY._serialized_end=217
  _TARGETCOWBOYS._serialized_start=219
  _TARGETCOWBOYS._serialized_end=265
  _COWBOYSERVICE._serialized_start=268
  _COWBOYSERVICE._serialized_end=469
# @@protoc_insertion_point(module_scope)