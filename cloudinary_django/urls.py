from django.conf.urls import url

from django.contrib import admin

admin.autodiscover()

import photo_album.views as photo_album

urlpatterns = [
    # URL for listing all images:
    url(r'^$', photo_album.list),
    url(r'^list$', photo_album.list, name='photo_album.views.list'),
    # URL for uploading an image
    url(r'^upload$', photo_album.upload, name='photo_album.views.upload'),
    # The direct upload functionality reports to this URL when an image is uploaded.
    url(r'^upload/complete$', photo_album.direct_upload_complete, name='photo_album.views.direct_upload_complete'),
    # Add the admin functionality:
    url(r'^admin/', admin.site.urls),
]
