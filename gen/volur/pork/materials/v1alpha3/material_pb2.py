# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: volur/pork/materials/v1alpha3/material.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2
from volur.pork.shared.v1alpha1 import characteristic_pb2 as volur_dot_pork_dot_shared_dot_v1alpha1_dot_characteristic__pb2
from volur.pork.shared.v1alpha1 import quantity_pb2 as volur_dot_pork_dot_shared_dot_v1alpha1_dot_quantity__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,volur/pork/materials/v1alpha3/material.proto\x12\x1dvolur.pork.materials.v1alpha3\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x17google/rpc/status.proto\x1a/volur/pork/shared/v1alpha1/characteristic.proto\x1a)volur/pork/shared/v1alpha1/quantity.proto\"\x98\x03\n\x08Material\x12\x1f\n\x0bmaterial_id\x18\x01 \x01(\tR\nmaterialId\x12\x14\n\x05plant\x18\x02 \x01(\tR\x05plant\x12@\n\x08quantity\x18\x03 \x01(\x0b\x32$.volur.pork.shared.v1alpha1.QuantityR\x08quantity\x12?\n\x04type\x18\x04 \x01(\x0e\x32+.volur.pork.materials.v1alpha3.MaterialTypeR\x04type\x12T\n\x0f\x63haracteristics\x18\x05 \x03(\x0b\x32*.volur.pork.shared.v1alpha1.CharacteristicR\x0f\x63haracteristics\x12=\n\narrived_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x02\x18\x01R\tarrivedAt\x12=\n\nexpires_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x02\x18\x01R\texpiresAt\"g\n UploadMaterialInformationRequest\x12\x43\n\x08material\x18\x01 \x01(\x0b\x32\'.volur.pork.materials.v1alpha3.MaterialR\x08material\"O\n!UploadMaterialInformationResponse\x12*\n\x06status\x18\x01 \x01(\x0b\x32\x12.google.rpc.StatusR\x06status*H\n\x0cMaterialType\x12\x1d\n\x19MATERIAL_TYPE_UNSPECIFIED\x10\x00\x12\x19\n\x15MATERIAL_TYPE_CARCASS\x10\x01\x32\xc1\x01\n\x1aMaterialInformationService\x12\xa2\x01\n\x19UploadMaterialInformation\x12?.volur.pork.materials.v1alpha3.UploadMaterialInformationRequest\x1a@.volur.pork.materials.v1alpha3.UploadMaterialInformationResponse(\x01\x30\x01\x42\x9b\x02\n!com.volur.pork.materials.v1alpha3B\rMaterialProtoP\x01ZPgithub.com/volur-ai/ryder/protos/volur/pork/materials/v1alpha3;materialsv1alpha3\xa2\x02\x03VPM\xaa\x02\x1dVolur.Pork.Materials.V1alpha3\xca\x02\x1dVolur\\Pork\\Materials\\V1alpha3\xe2\x02)Volur\\Pork\\Materials\\V1alpha3\\GPBMetadata\xea\x02 Volur::Pork::Materials::V1alpha3b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'volur.pork.materials.v1alpha3.material_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n!com.volur.pork.materials.v1alpha3B\rMaterialProtoP\001ZPgithub.com/volur-ai/ryder/protos/volur/pork/materials/v1alpha3;materialsv1alpha3\242\002\003VPM\252\002\035Volur.Pork.Materials.V1alpha3\312\002\035Volur\\Pork\\Materials\\V1alpha3\342\002)Volur\\Pork\\Materials\\V1alpha3\\GPBMetadata\352\002 Volur::Pork::Materials::V1alpha3'
  _globals['_MATERIAL'].fields_by_name['arrived_at']._loaded_options = None
  _globals['_MATERIAL'].fields_by_name['arrived_at']._serialized_options = b'\030\001'
  _globals['_MATERIAL'].fields_by_name['expires_at']._loaded_options = None
  _globals['_MATERIAL'].fields_by_name['expires_at']._serialized_options = b'\030\001'
  _globals['_MATERIALTYPE']._serialized_start=826
  _globals['_MATERIALTYPE']._serialized_end=898
  _globals['_MATERIAL']._serialized_start=230
  _globals['_MATERIAL']._serialized_end=638
  _globals['_UPLOADMATERIALINFORMATIONREQUEST']._serialized_start=640
  _globals['_UPLOADMATERIALINFORMATIONREQUEST']._serialized_end=743
  _globals['_UPLOADMATERIALINFORMATIONRESPONSE']._serialized_start=745
  _globals['_UPLOADMATERIALINFORMATIONRESPONSE']._serialized_end=824
  _globals['_MATERIALINFORMATIONSERVICE']._serialized_start=901
  _globals['_MATERIALINFORMATIONSERVICE']._serialized_end=1094
# @@protoc_insertion_point(module_scope)
