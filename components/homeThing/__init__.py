import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.components import display, font, color, wifi, api, binary_sensor
from esphome.const import  CONF_ID, CONF_TRIGGER_ID, CONF_INTERVAL
from esphome.components.homeassistant_media_player import homeassistant_media_player_ns
from esphome.components.homeassistant_light_group import homeassistant_light_group_ns
from esphome.components.homeassistant_service_group import homeassistant_service_group_ns
from esphome.components.homeassistant_sensor_group import homeassistant_sensor_group_ns
from esphome.components.homeassistant_switch_group import homeassistant_switch_group_ns
homething_menu_base_ns = cg.esphome_ns.namespace("homething_menu_base")

HomeThingMenuBase = homething_menu_base_ns.class_("HomeThingMenuBase", cg.PollingComponent)
HomeThingMenuBoot = homething_menu_base_ns.class_("HomeThingMenuBoot")
HomeThingMenuAnimation = homething_menu_base_ns.class_("HomeThingMenuAnimation")
HomeThingMenuDisplay = homething_menu_base_ns.class_("HomeThingMenuDisplay")
HomeThingMenuDisplayState = homething_menu_base_ns.class_("HomeThingMenuDisplayState")
HomeThingMenuHeader = homething_menu_base_ns.class_("HomeThingMenuHeader")
HomeThingMenuTextHelpers = homething_menu_base_ns.class_("HomeThingMenuTextHelpers")
HomeThingMenuRefactor = homething_menu_base_ns.class_("HomeThingMenuRefactor")
HomeThingMenuNowPlaying = homething_menu_base_ns.class_("HomeThingMenuNowPlaying")

HomeThingMenuBaseConstPtr = HomeThingMenuBase.operator("ptr").operator("const")
HomeThingDisplayMenuOnRedrawTrigger = homething_menu_base_ns.class_("HomeThingDisplayMenuOnRedrawTrigger", automation.Trigger)

CONF_DISPLAY = "display"
CONF_MENU_DISPLAY = "menu_display"
CONF_DISPLAY_STATE = "display_state"
CONF_TEXT_HELPERS = "text_helpers"
CONF_REFACTOR = "refactor_me"
CONF_NOW_PLAYING = "now_playing"
CONF_FONT_SMALL = "font_small"
CONF_FONT_MEDIUM = "font_medium"
CONF_FONT_LARGE = "font_large"
CONF_FONT_LARGE_HEAVY = "font_large_heavy"
CONF_FONT_MATERIAL_LARGE = "font_material_large"
CONF_FONT_MATERIAL_SMALL = "font_material_small"
CONF_FONT_LOGO = "font_logo"
CONF_WIFI = "wifi"
CONF_API = "api"
CONF_BOOT = "boot"
CONF_HEADER = "header"
CONF_MENU_Display = "menu_display"
CONF_MEDIA_PLAYERS = "media_players"
CONF_LIGHTS = "lights"
CONF_SERVICES = "services"
CONF_SENSORS = "sensors"
CONF_SWITCHES = "switches"
CONF_ON_REDRAW = "on_redraw"
CONF_IDLE_TICK = "idle_tick"

DEPENDENCIES = ["wifi", "api"]

BOOT_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(HomeThingMenuBoot),
        cv.Required(CONF_WIFI): cv.use_id(binary_sensor.BinarySensor),
        cv.Required(CONF_API): cv.use_id(binary_sensor.BinarySensor),
    }
)

MENU_DISPLAY_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(HomeThingMenuDisplay),
        cv.GenerateID(CONF_TEXT_HELPERS): cv.declare_id(HomeThingMenuTextHelpers),
        cv.GenerateID(CONF_REFACTOR): cv.declare_id(HomeThingMenuRefactor),
        cv.GenerateID(CONF_NOW_PLAYING): cv.declare_id(HomeThingMenuNowPlaying),
        # cv.GenerateID(CONF_BOOT): cv.use_id(HomeThingMenuBoot),
        cv.GenerateID(CONF_HEADER): cv.declare_id(HomeThingMenuHeader),
    }
)

DISPLAY_STATE_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(HomeThingMenuDisplayState),
        cv.Required(CONF_FONT_SMALL): cv.use_id(font.Font),
        cv.Required(CONF_FONT_MEDIUM): cv.use_id(font.Font),
        cv.Required(CONF_FONT_LARGE): cv.use_id(font.Font),
        cv.Required(CONF_FONT_LARGE_HEAVY): cv.use_id(font.Font),
        cv.Required(CONF_FONT_MATERIAL_LARGE): cv.use_id(font.Font),
        cv.Required(CONF_FONT_MATERIAL_SMALL): cv.use_id(font.Font),
        cv.Required(CONF_FONT_LOGO): cv.use_id(font.Font),
    }
)

HEADER_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(HomeThingMenuHeader),
    }
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(HomeThingMenuBase),
        # cv.GenerateID(CONF_IDLE_TICK): IDLE_TICK_SCHEMA,
        cv.Required(CONF_DISPLAY): cv.use_id(display.DisplayBuffer),
        cv.Required(CONF_DISPLAY_STATE): DISPLAY_STATE_SCHEMA,
        cv.Optional(CONF_HEADER, default={}): HEADER_SCHEMA,
        cv.Optional(CONF_MENU_Display, default={}): MENU_DISPLAY_SCHEMA,
        cv.Required(CONF_MEDIA_PLAYERS): cv.use_id(homeassistant_media_player_ns.HomeAssistantMediaPlayerGroup),
        cv.Required(CONF_LIGHTS): cv.use_id(homeassistant_light_group_ns.HomeAssistantLightGroup),
        cv.Required(CONF_SERVICES): cv.use_id(homeassistant_light_group_ns.HomeAssistantServiceGroup),
        cv.Required(CONF_SWITCHES): cv.use_id(homeassistant_switch_group_ns.HomeAssistantSwitchGroup),
        cv.Required(CONF_SENSORS): cv.use_id(homeassistant_light_group_ns.HomeAssistantSensorsGroup),
        cv.GenerateID(CONF_BOOT): BOOT_SCHEMA,
        cv.Optional(CONF_ON_REDRAW): automation.validate_automation(
            {
                cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(
                    HomeThingDisplayMenuOnRedrawTrigger
                )
            }
        )
        # cv.GenerateID(CONF_MENU_DISPLAY): MENU_DISPLAY_SCHEMA
    }
).extend(cv.polling_component_schema("1s"))

async def display_state_to_code(config):
    display_state = cg.new_Pvariable(config[CONF_ID])

    menu_font_small = await cg.get_variable(config[CONF_FONT_SMALL])
    cg.add(display_state.set_small_font(menu_font_small))

    menu_font_medium = await cg.get_variable(config[CONF_FONT_MEDIUM])
    cg.add(display_state.set_medium_font(menu_font_medium))

    menu_font_large = await cg.get_variable(config[CONF_FONT_LARGE])
    cg.add(display_state.set_large_font(menu_font_large))

    menu_font_large_heavy = await cg.get_variable(config[CONF_FONT_LARGE_HEAVY])
    cg.add(display_state.set_large_heavy_font(menu_font_large_heavy))

    menu_font_material_large = await cg.get_variable(config[CONF_FONT_MATERIAL_LARGE])
    cg.add(display_state.set_material_font_large(menu_font_material_large))

    menu_font_material_small = await cg.get_variable(config[CONF_FONT_MATERIAL_SMALL])
    cg.add(display_state.set_material_font_small(menu_font_material_small))

    menu_font_logo = await cg.get_variable(config[CONF_FONT_LOGO])
    cg.add(display_state.set_menu_font_logo(menu_font_logo))
    return display_state

async def text_helpers_to_code(config, display_buffer, display_state):
    text_helpers = cg.new_Pvariable(config)
    cg.add(text_helpers.set_display_buffer(display_buffer))
    cg.add(text_helpers.set_display_state(display_state))
    # HomeThingMenuTextHelpers(display_buffer_, display_state_);
    return text_helpers

async def menu_boot_to_code(config, display_buffer, display_state, media_players, menu_header):
    menu_boot = cg.new_Pvariable(config[CONF_ID], display_buffer, display_state, menu_header, media_players)

    wifi_sensor = await cg.get_variable(config[CONF_WIFI])
    cg.add(menu_boot.set_wifi_connected(wifi_sensor))

    api_sensor = await cg.get_variable(config[CONF_API])
    cg.add(menu_boot.set_api_connected(api_sensor))

    return menu_boot

    #   display::DisplayBuffer* display_buffer,
    #   HomeThingMenuDisplayState* display_state,
    #   HomeThingMenuTextHelpers* text_helpers, HomeThingMenuRefactor* refactor,
    #   HomeThingMenuNowPlaying* now_playing, HomeThingMenuHeader* header,
    #   HomeThingMenuBoot* boot,
    #   homeassistant_media_player::HomeAssistantMediaPlayerGroup*
    #       new_speaker_group)
async def menu_display_to_code(config, display_buffer, media_players, lights, services, sensors, switches):
    menu_display_conf = config[CONF_MENU_DISPLAY]

    display_state = await display_state_to_code(config[CONF_DISPLAY_STATE])
    text_helpers = await text_helpers_to_code(menu_display_conf[CONF_TEXT_HELPERS], display_buffer, display_state)
    refactor = cg.new_Pvariable(menu_display_conf[CONF_REFACTOR], display_buffer, display_state, text_helpers)
    now_playing = cg.new_Pvariable(menu_display_conf[CONF_NOW_PLAYING], display_buffer, display_state, text_helpers, media_players)
    menu_header = cg.new_Pvariable(menu_display_conf[CONF_HEADER], display_buffer, display_state, text_helpers, media_players, lights)
    menu_boot = await menu_boot_to_code(config[CONF_BOOT], display_buffer, display_state, media_players, menu_header)

    menu_display = cg.new_Pvariable(menu_display_conf[CONF_ID], display_buffer, display_state, text_helpers, refactor, now_playing, menu_header, menu_boot, media_players, lights, services, sensors, switches)
    return menu_display

async def to_code(config):
    media_players = await cg.get_variable(config[CONF_MEDIA_PLAYERS])
    lights = await cg.get_variable(config[CONF_LIGHTS])
    services = await cg.get_variable(config[CONF_SERVICES])
    sensors = await cg.get_variable(config[CONF_SENSORS])
    switches = await cg.get_variable(config[CONF_SWITCHES])
    display_buffer = await cg.get_variable(config[CONF_DISPLAY])
    menu_display = await menu_display_to_code(config, display_buffer, media_players, lights, services, sensors, switches)

    # idle_tick = cg.new_Pvariable(config[CONF_IDLE_TICK])
    menu = cg.new_Pvariable(config[CONF_ID], menu_display, media_players, lights, services, sensors, switches)
    await cg.register_component(menu, config)
    for conf in config.get(CONF_ON_REDRAW, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], menu)
        await automation.build_automation(trigger, [(HomeThingMenuBaseConstPtr, "it")], conf)


    # animation = await menu_animation_to_code(menu)

   
