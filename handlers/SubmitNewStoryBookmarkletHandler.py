#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#Copyright (c) 2011 - Santiago Zavala
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import logging
import hashlib
import prefetch
import helper
import random

from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template
from google.appengine.ext.webapp.util import run_wsgi_app

from datetime import datetime, date, timedelta
from gaesessions import get_current_session
from django.utils import simplejson

from libs import PyRSS2Gen
from models import User, Post, Comment, Vote, Notification, Ticket


#register the desdetiempo filter to print time since in spanish
template.register_template_library('filters.CustomFilters')

class Handler(webapp.RequestHandler):
  def get(self):
    session = get_current_session()
    if session.has_key('post_error'):
      post_error = session.pop('post_error')

    url = self.request.get('url')
    title = helper.sanitizeHtml(self.request.get('title'))
    nice_url = helper.sluglify(title)
 
    if session.has_key('user'):
      if len(nice_url) > 0:
        user = session['user']
        #Check that we don't have the same URL within the last 'check_days'
        since_date = date.today() - timedelta(days=7)
        q = Post.all().filter("created >", since_date).filter("url =", url).count()
        url_exists = q > 0
        q = Post.all().filter("nice_url", nice_url).count()
        nice_url_exist = q > 0
        try:
          if not url_exists:
            if not nice_url_exist:
              post = Post(
                  url=url,
                  title=title,
                  message='bookmarklet',
                  user=user,
                  nice_url=nice_url
                  )
              post.put()
              vote = Vote(user=user, post=post, target_user=post.user)
              vote.put()
              Post.remove_cached_count_from_memcache()

              #index with indextank
              helper.indextank_document( helper.base_url(self), post)
              
              logging.debug('redirecting to'+str(post.nice_url))
              self.redirect('/noticia/' + str(post.nice_url));
            else:
              session['post_error'] = "Este titulo ha sido usado en una noticia anterior"
              self.redirect('/agregar')
          else:
            session['post_error'] = "Este link ha sido entregado en los ultimo 7 dias"
            self.redirect('/agregar')
        except db.BadValueError:
          session['post_error'] = "El formato del link no es valido"
          self.redirect('/agregar')
    else:
      session['login_error'] = "Inicia sesión para agregar una noticia"
      self.redirect('/login')
