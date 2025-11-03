from django.contrib import admin
from blog.models import Post, Comment, Category
from import_export.admin import ImportExportModelAdmin
from django_ckeditor_5.widgets import CKEditor5Widget



class ArticleAdmin(ImportExportModelAdmin):
	search_fields = ['title']
	list_editable = ['status', 'category']
	list_filter = ('category', 'status', 'featured', 'trending', 'date')
	list_display = ('title', 'status', 'category', 'user', 'featured', 'trending', 'date', 'views')
	readonly_fields = ('pid', 'views', 'date')

	fieldsets = (
		('Basic Information', {
			'fields': ('title', 'user', 'category', 'image')
		}),
		('Content', {
			'fields': ('excerpt', 'content')
		}),
		('Settings', {
			'fields': ('status', 'featured', 'trending', 'tags')
		}),
		('Metadata', {
			'fields': ('pid', 'views', 'date'),
			'classes': ('collapse',)
		}),
	)

	def title(self):
		return self.title[0:10]

class CategoryAdmin(ImportExportModelAdmin):
	prepopulated_fields = {'slug':('title',)}
	list_display = ('title', 'active')

class CommentAdmin(ImportExportModelAdmin):
	search_fields = ['comment']
	list_editable = ('active',)
	list_filter = ('active',)
	list_display = ('post', 'active')


admin.site.register(Post, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)