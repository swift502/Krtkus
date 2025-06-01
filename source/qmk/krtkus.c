#include "krtkus.h"

void press_code(keyrecord_t *record, uint16_t keycode)
{
    if (record->event.pressed)
    {
        register_code(keycode);
    }
    else
    {
        unregister_code(keycode);
    }
}

bool process_record_kb(uint16_t keycode, keyrecord_t *record)
{
    uint8_t mods = get_mods();
    bool double_shift = (mods & MOD_MASK_SHIFT) == MOD_MASK_SHIFT;

    switch (keycode)
    {
        case KRT_VOL:
            if (mods & MOD_MASK_CTRL)
            {
                press_code(record, KC_MUTE);
            }
            else if (mods & MOD_MASK_SHIFT)
            {
                press_code(record, KC_VOLU);
            }
            else
            {
                press_code(record, KC_VOLD);
            }
            return false;

        case KC_B:
            if (record->event.pressed && double_shift)
            {
                reset_keyboard();
                return false;
            }
            break;

        case KC_C:
            if (record->event.pressed && double_shift)
            {
                eeconfig_init();
                soft_reset_keyboard();
                return false;
            }
            break;
    }

    return process_record_user(keycode, record);
}