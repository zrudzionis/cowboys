def protobuf_to_dict(proto_obj):
    return {
        key: getattr(proto_obj, key)
        for key in proto_obj.DESCRIPTOR.fields_by_name.keys()
    }
