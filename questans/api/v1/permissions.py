from rest_framework import permissions


class CustomModelPermissions(permissions.BasePermission):
	"""
	Custom permissions for different actions
	"""
	# has_permission refers to permissions that don't involve only a single object e.g list, create 
	# while has_object_permission refers to permissions pertaining to a single object e.g retrieve, update, delete
	def has_permission(self, request, view):
		if view.action == 'create':
			return request.user.is_authenticated

		return True

	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request
		# so we'll always allow GET, HEAD or OPTIONS requests.
		# if request.method in permissions.SAFE_METHODS:
		# 	return True

		if view.action in ('update', 'partial_update', 'destroy'):
			return obj.user == request.user or request.user.is_superuser

		return True

