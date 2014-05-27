#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

import uuid
from urlparse import urljoin
from django.core.urlresolvers import reverse_lazy
from django.core.mail import EmailMessage
from django.core.cache import cache

def send_confirm_email(user_email, site):
    """ 注册提交信息后向用户发送注册确认邮件， 只有通过邮件确认后才可以登录
    """
    token = uuid.uuid4().hex
    cache.set(token, user_email, 600)
    print token
    print cache.get(token)
    subject = "请验证邮箱-{}".format(site.name.encode("utf-8"))
    confirm_link = urljoin(site.link(), reverse_lazy("confirm_mail").lower())
    content = """
            <p>有人使用您的邮箱在{0}注册帐号，如果不是您，请忽略此邮件</p><br />
            <p>点击下面链接确认邮箱</p>
            <p><a href="{1}?token={2}">{1}?token={2}</a></p>
            <p>链接十分钟内有效！</p>
            """.format(site, confirm_link, token)
    from_email = "no-reply@mail.{}".format(site.domain)
    msg = EmailMessage(subject, content, from_email, [user_email])
    msg.content_subtype = "html"
    msg.send()