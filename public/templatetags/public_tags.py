from django import template

from public.classname import classname
from public.current_url_fully_qualified import current_url_fully_qualified
from public.home_nav_boxes import home_nav_boxes
from public.home_showcase import home_showcase
from public.home_showcase_item_prisoner import home_showcase_item_prisoner
from public.home_showcase_item_featured_news import home_showcase_item_featured_news
from public.information_overlay import information_overlay
from public.information_overlay_trigger_button import information_overlay_trigger_button
from public.nav_header import nav_header
from public.inject_search_variables import inject_search_variables


register = template.Library()

register.simple_tag(
    takes_context=True
)(inject_search_variables)

register.simple_tag(
    takes_context=True
)(classname)

register.simple_tag(
    takes_context=True
)(current_url_fully_qualified)

register.simple_tag(
    takes_context=True
)(home_nav_boxes)

register.simple_tag(
    takes_context=True
)(home_showcase)

register.simple_tag(
    takes_context=True
)(home_showcase_item_prisoner)

register.simple_tag(
    takes_context=True
)(home_showcase_item_featured_news)

register.simple_tag(
    takes_context=True
)(information_overlay)

register.simple_tag(
    takes_context=True
)(information_overlay_trigger_button)

register.simple_tag(
    takes_context=True
)(nav_header)
