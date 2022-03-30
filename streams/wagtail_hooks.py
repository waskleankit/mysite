import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.core import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import (
InlineStyleElementHandler
)
@hooks.register("register_rich_text_features")
def register_code_styling(features):
    """Add the <code> to the richtext editor."""

    # step1
    feature_name = "code"
    type_ = "CODE"
    tag = "code"

    # step2
    control = {
        "type": type_,
        "label": "</>",
        "description": "Code"
    }

    # step3
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    # step 4
    db_conversion = {
        "from_database_formate": {tag: InlineStyleElementHandler(type_)},
        "to_database_formate": {"stylemap": {type_:{"element": tag}}}
    }

    #step 5
    features.register_converter_rule("contentstate", feature_name, db_conversion)


    # step 6 optional
    # This will register this feature with all richtext editors by default
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """Creates centered text n our richtext."""

    feature_name = "center"
    type_ = "CENTERTEXT"
    tag = "div"

    control = {
        "type": type_,
        "label":"Center",
        "description": "Center Text",
        "style":{
            "display": "block",
            "text-align": "center",
        },
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_:{
                    "element": tag,
                    "props": {
                        "class":"d-block text-center"

                    }
                }
            }
        }
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)