def get_ids(queryset):
    return [
        object_id
        for object_id in queryset.split(",")
    ]
