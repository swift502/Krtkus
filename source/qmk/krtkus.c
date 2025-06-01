#include "krtkus.h"

bool process_record_kb(uint16_t keycode, keyrecord_t *record)
{
    uint8_t mods = get_mods();
    bool double_shift = (mods & MOD_MASK_SHIFT) == MOD_MASK_SHIFT;

    switch (keycode)
    {
        case KRT_VOL:
            if (record->event.pressed)
            {
                if (mods & MOD_MASK_CTRL)
                {
                    register_code(KC_MUTE);
                }
                else if (mods & MOD_MASK_SHIFT)
                {
                    register_code(KC_VOLU);
                }
                else
                {
                    register_code(KC_VOLD);
                }
            }
            else
            {
                host_consumer_send(0);
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