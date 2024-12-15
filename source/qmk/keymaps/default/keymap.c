#include QMK_KEYBOARD_H

enum keyboard_keycodes
{
    KRT_VOL = QK_KB_0
};

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
                    tap_code(KC_MUTE);
                    return false;
                }

                if (mods & MOD_MASK_SHIFT)
                {
                    tap_code(KC_VOLU);
                    return false;
                }

                tap_code(KC_VOLD);
                return false;
            }
            break;

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

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    /*
     * ┌───┐                                       ┌───┐
     * │ ` │                                       │Del│
     * ├───┼───┬───┬───┬───┬───┬───┬───┬───┬───┬───┼───┤
     * │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 0 │ - │ = │
     * ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
     * │Tab│ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │Bsp│
     * ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
     * │Esc│ A │ S │ D │ F │ G │ H │ J │ K │ L │ ; │ ' │
     * ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
     * │Sft│ Z │ X │ C │ V │ B │ N │ M │ , │ . │ / │Ent│
     * ├───┼───┼───┼───┼───┼───┴───┼───┼───┼───┼───┼───┤
     * │Ctl│GUI│Vol│Alt│Lwr│ Space │Rse│ ← │ ↓ │ ↑ │ → │
     * └───┴───┴───┴───┴───┴───────┴───┴───┴───┴───┴───┘
     */
    [0] = LAYOUT_default(
        KC_GRV,                                                                                            KC_DEL,
        KC_1,    KC_2,    KC_3,    KC_4,    KC_5,    KC_6,    KC_7,    KC_8,    KC_9,    KC_0,    KC_MINS, KC_EQL,
        KC_TAB,  KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,    KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,    KC_BSPC,
        KC_ESC,  KC_A,    KC_S,    KC_D,    KC_F,    KC_G,    KC_H,    KC_J,    KC_K,    KC_L,    KC_SCLN, KC_QUOT,
        KC_LSFT, KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,    KC_N,    KC_M,    KC_COMM, KC_DOT,  KC_SLSH, SC_SENT,
        KC_LCTL, KC_LGUI, KRT_VOL, KC_LALT, MO(1),        KC_SPC,      MO(2),   KC_LEFT, KC_DOWN, KC_UP,   KC_RGHT
    ),
    [1] = LAYOUT_default(
        _______,                                                                                           _______,
        KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,   KC_F6,   KC_F7,   KC_F8,   KC_F9,   KC_F10,  KC_F11,  KC_F12,
        _______, _______, KC_UP,   _______, _______, KC_KP_7, KC_KP_8, KC_KP_9, _______, _______, KC_LBRC, KC_RBRC,
        KC_CAPS, KC_LEFT, KC_DOWN, KC_RGHT, _______, KC_KP_4, KC_KP_5, KC_KP_6, _______, _______, _______, KC_BSLS,
        _______, _______, _______, _______, _______, KC_KP_1, KC_KP_2, KC_KP_3, _______, _______, _______, KC_ENT,
        _______, _______, _______, _______, _______,      KC_KP_0,     KC_PDOT, KC_HOME, KC_PGDN, KC_PGUP, KC_END
    ),
    [2] = LAYOUT_default(
        _______,                                                                                           _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, KC_MUTE, KC_VOLD, KC_VOLU,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, KC_LBRC, KC_RBRC,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, KC_BSLS,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, RSFT(KC_ENT),
        _______, _______, _______, _______, _______,      _______,     _______, _______, _______, _______, _______
    ),
    [3] = LAYOUT_default(
        _______,                                                                                           _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______,      _______,     _______, _______, _______, _______, _______
    )
};
