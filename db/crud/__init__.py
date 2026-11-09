from db.crud import user
from db.crud import role
from db.crud import article
from db.crud import tag
from db.crud import m2m_relationships

from db.crud.user import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    deactive_user,
)
from db.crud.role import (
    create_role,
    get_role_by_id,
    get_all_roles,
    update_role,
    delete_role,
)
from db.crud.article import (
    create_article,
    get_article_by_id,
    get_all_articles,
    update_article,
    delete_article,
)
from db.crud.tag import (
    create_tag,
    get_tag_by_id,
    get_all_tags,
    update_tag,
    delete_tag,
)
from db.crud.m2m_relationships import (
    add_tag_to_article,
    remove_tag_from_article,
    get_article_tags,
    get_articles_by_tag,
    like_article,
    unlike_article,
    get_article_likes,
    get_user_likes,
    subscribe_to_tag,
    unsubscribe_from_tag,
    get_user_subscriptions,
    get_tag_subscriptions,
    set_notification,
    get_notification_recipients,
    get_notification_recipients_for_article,
    get_user_notification_settings,
)

__all__ = [
    # user
    "create_user", "get_user_by_id", "get_all_users", "update_user", "deactive_user",
    # role
    "create_role", "get_role_by_id", "get_all_roles", "update_role", "delete_role",
    # article
    "create_article", "get_article_by_id", "get_all_articles", "update_article", "delete_article",
    # tag
    "create_tag", "get_tag_by_id", "get_all_tags", "update_tag", "delete_tag",
    # m2m
    "add_tag_to_article", "remove_tag_from_article", "get_article_tags",
    "get_articles_by_tag", "like_article", "unlike_article", "get_article_likes",
    "get_user_likes", "subscribe_to_tag", "unsubscribe_from_tag",
    "get_user_subscriptions", "get_tag_subscriptions", "set_notification",
    "get_notification_recipients", "get_notification_recipients_for_article",
    "get_user_notification_settings",
]