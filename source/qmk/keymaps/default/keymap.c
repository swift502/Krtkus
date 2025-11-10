#include QMK_KEYBOARD_H

#define SE_LEFT MT(MOD_LSFT, KC_ENT)
#define SE_RGHT MT(MOD_RSFT, KC_ENT)

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
        KC_LSFT, KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,    KC_N,    KC_M,    KC_COMM, KC_DOT,  KC_SLSH, SE_RGHT,
        KC_LCTL, KC_LGUI, KRT_VOL, KC_LALT, MO(1),        KC_SPC,      MO(2),   KC_LEFT, KC_DOWN, KC_UP,   KC_RGHT
    ),
    [1] = LAYOUT_default(
        _______,                                                                                           KC_NUM,
        KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,   KC_F6,   KC_F7,   KC_F8,   KC_F9,   KC_F10,  KC_F11,  KC_F12,
        KC_INS,  _______, KC_UP,   _______, KC_PGUP, KC_P7,   KC_P8,   KC_P9,   _______, _______, _______, _______,
        KC_CAPS, KC_LEFT, KC_DOWN, KC_RGHT, KC_PGDN, KC_P4,   KC_P5,   KC_P6,   _______, KC_LBRC, KC_RBRC, KC_BSLS,
        SE_LEFT, _______, _______, _______, _______, KC_P1,   KC_P2,   KC_P3,   _______, _______, _______, _______,
        _______, _______, _______, _______, _______,      KC_P0,       KC_PDOT, KC_HOME, _______, _______, KC_END
    ),
    [2] = LAYOUT_default(
        _______,                                                                                           KC_PSCR,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, KC_MUTE, KC_VOLD, KC_VOLU,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, KC_PSLS, KC_PAST, KC_PMNS,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, KC_PPLS,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, RSFT(KC_ENT),
        _______, _______, _______, _______, _______,      _______,     _______, _______, _______, _______, RCTL(KC_ENT)
    )
};
