# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: volur/pork/materials/v1alpha2/material.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2
from volur.pork.materials.v1alpha2 import characteristic_pb2 as volur_dot_pork_dot_materials_dot_v1alpha2_dot_characteristic__pb2
from volur.pork.materials.v1alpha2 import quantity_pb2 as volur_dot_pork_dot_materials_dot_v1alpha2_dot_quantity__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,volur/pork/materials/v1alpha2/material.proto\x12\x1dvolur.pork.materials.v1alpha2\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x17google/rpc/status.proto\x1a\x32volur/pork/materials/v1alpha2/characteristic.proto\x1a,volur/pork/materials/v1alpha2/quantity.proto\"\x96\x03\n\x08Material\x12\x1f\n\x0bmaterial_id\x18\x01 \x01(\tR\nmaterialId\x12\x14\n\x05plant\x18\x02 \x01(\tR\x05plant\x12\x43\n\x08quantity\x18\x03 \x01(\x0b\x32\'.volur.pork.materials.v1alpha2.QuantityR\x08quantity\x12?\n\x04type\x18\x06 \x01(\x0e\x32+.volur.pork.materials.v1alpha2.MaterialTypeR\x04type\x12W\n\x0f\x63haracteristics\x18\x07 \x03(\x0b\x32-.volur.pork.materials.v1alpha2.CharacteristicR\x0f\x63haracteristics\x12\x39\n\narrived_at\x18\t \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tarrivedAt\x12\x39\n\nexpires_at\x18\n \x01(\x0b\x32\x1a.google.protobuf.TimestampR\texpiresAt\"g\n UploadMaterialInformationRequest\x12\x43\n\x08material\x18\x01 \x01(\x0b\x32\'.volur.pork.materials.v1alpha2.MaterialR\x08material\"O\n!UploadMaterialInformationResponse\x12*\n\x06status\x18\x01 \x01(\x0b\x32\x12.google.rpc.StatusR\x06status*H\n\x0cMaterialType\x12\x1d\n\x19MATERIAL_TYPE_UNSPECIFIED\x10\x00\x12\x19\n\x15MATERIAL_TYPE_CARCASS\x10\x01\x32\xc1\x01\n\x1aMaterialInformationService\x12\xa2\x01\n\x19UploadMaterialInformation\x12?.volur.pork.materials.v1alpha2.UploadMaterialInformationRequest\x1a@.volur.pork.materials.v1alpha2.UploadMaterialInformationResponse(\x01\x30\x01\x42\xb0\x02\n!com.volur.pork.materials.v1alpha2B\rMaterialProtoP\x01Zegithub.com/volur-ai/data-component-cooperl/api/protos/volur/pork/materials/v1alpha2;materialsv1alpha2\xa2\x02\x03VPM\xaa\x02\x1dVolur.Pork.Materials.V1alpha2\xca\x02\x1dVolur\\Pork\\Materials\\V1alpha2\xe2\x02)Volur\\Pork\\Materials\\V1alpha2\\GPBMetadata\xea\x02 Volur::Pork::Materials::V1alpha2b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'volur.pork.materials.v1alpha2.material_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n!com.volur.pork.materials.v1alpha2B\rMaterialProtoP\001Zegithub.com/volur-ai/data-component-cooperl/api/protos/volur/pork/materials/v1alpha2;materialsv1alpha2\242\002\003VPM\252\002\035Volur.Pork.Materials.V1alpha2\312\002\035Volur\\Pork\\Materials\\V1alpha2\342\002)Volur\\Pork\\Materials\\V1alpha2\\GPBMetadata\352\002 Volur::Pork::Materials::V1alpha2'
  _globals['_MATERIALTYPE']._serialized_start=830
  _globals['_MATERIALTYPE']._serialized_end=902
  _globals['_MATERIAL']._serialized_start=236
  _globals['_MATERIAL']._serialized_end=642
  _globals['_UPLOADMATERIALINFORMATIONREQUEST']._serialized_start=644
  _globals['_UPLOADMATERIALINFORMATIONREQUEST']._serialized_end=747
  _globals['_UPLOADMATERIALINFORMATIONRESPONSE']._serialized_start=749
  _globals['_UPLOADMATERIALINFORMATIONRESPONSE']._serialized_end=828
  _globals['_MATERIALINFORMATIONSERVICE']._serialized_start=905
  _globals['_MATERIALINFORMATIONSERVICE']._serialized_end=1098
# @@protoc_insertion_point(module_scope)