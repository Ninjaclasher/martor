import markdown
from django.templatetags.static import static

from ..settings import (MARTOR_MARKDOWN_BASE_EMOJI_URL,
                        MARTOR_MARKDOWN_BASE_EMOJI_USE_STATIC)

"""
>>> import markdown
>>> md = markdown.Markdown(extensions=['martor.utils.extensions.emoji'])
>>> md.convert(':smile:')
'<p><img class="marked-emoji" src="https://www.webfx.com/tools/emoji-cheat-sheet/graphics/emojis/smile.png" /></p>'
>>>
"""

EMOJI_RE = r'(:[+\-\w]+:)'
EMOJIS = [':yellow_heart:', ':blue_heart:', ':purple_heart:', ':heart:', ':green_heart:', ':broken_heart:', ':heartbeat:',
          ':heartpulse:', ':two_hearts:', ':revolving_hearts:', ':cupid:', ':sparkling_heart:', ':sparkles:', ':star:',
          ':star2:', ':dizzy:', ':boom:', ':collision:', ':anger:', ':exclamation:', ':question:', ':grey_exclamation:',
          ':grey_question:', ':zzz:', ':dash:', ':sweat_drops:', ':notes:', ':musical_note:', ':fire:', ':thumbsup:',
          ':-1:', ':thumbsdown:', ':ok_hand:', ':punch:', ':facepunch:', ':fist:', ':v:', ':wave:', ':hand:', ':raised_hand:',
          ':open_hands:', ':point_up:', ':point_down:', ':point_left:', ':point_right:', ':raised_hands:', ':pray:', ':point_up_2:',
          ':clap:', ':muscle:', ':nail_care:', ':sunny:', ':umbrella:', ':cloud:', ':snowflake:', ':zap:',
          ':cyclone:', ':foggy:', ':ocean:', ':bouquet:', ':cherry_blossom:', ':tulip:', ':four_leaf_clover:', ':rose:',
          ':sunflower:', ':hibiscus:', ':maple_leaf:', ':leaves:', ':fallen_leaf:', ':herb:', ':mushroom:', ':cactus:',
          ':palm_tree:', ':evergreen_tree:', ':deciduous_tree:', ':chestnut:', ':seedling:', ':blossom:', ':ear_of_rice:',
          ':shell:', ':globe_with_meridians:', ':new_moon:', ':waxing_crescent_moon:', ':first_quarter_moon:', ':waxing_gibbous_moon:',
          ':full_moon:', ':waning_gibbous_moon:', ':last_quarter_moon:', ':waning_crescent_moon:', ':last_quarter_moon_with_face:',
          ':first_quarter_moon_with_face:', ':crescent_moon:', ':earth_africa:', ':earth_americas:', ':earth_asia:', ':volcano:',
          ':milky_way:', ':partly_sunny:', ':bamboo:', ':gift_heart:', ':school_satchel:', ':mortar_board:', ':flags:', ':fireworks:',
          ':sparkler:', ':wind_chime:', ':rice_scene:', ':gift:', ':bell:', ':no_bell:', ':tanabata_tree:', ':tada:', ':confetti_ball:',
          ':balloon:', ':crystal_ball:', ':cd:', ':dvd:', ':floppy_disk:', ':camera:', ':video_camera:', ':movie_camera:', ':computer:',
          ':tv:', ':iphone:', ':phone:', ':telephone:', ':telephone_receiver:', ':pager:', ':fax:', ':minidisc:', ':vhs:', ':sound:',
          ':speaker:', ':mute:', ':loudspeaker:', ':mega:', ':hourglass:', ':hourglass_flowing_sand:', ':alarm_clock:', ':watch:',
          ':radio:', ':satellite:', ':loop:', ':mag:', ':mag_right:', ':unlock:', ':lock:', ':lock_with_ink_pen:', ':closed_lock_with_key:',
          ':key:', ':bulb:', ':flashlight:', ':high_brightness:', ':low_brightness:', ':electric_plug:', ':battery:', ':calling:', ':email:',
          ':mailbox:', ':postbox:', ':bath:', ':bathtub:', ':shower:', ':toilet:', ':wrench:', ':nut_and_bolt:', ':hammer:', ':seat:',
          ':moneybag:', ':yen:', ':dollar:', ':pound:', ':euro:', ':credit_card:', ':money_with_wings:', ':e-mail:', ':inbox_tray:',
          ':outbox_tray:', ':envelope:', ':incoming_envelope:', ':postal_horn:', ':mailbox_closed:', ':mailbox_with_mail:', ':mailbox_with_no_mail:',
          ':package:', ':door:', ':smoking:', ':bomb:', ':gun:', ':hocho:', ':pill:', ':syringe:', ':page_facing_up:', ':page_with_curl:',
          ':bookmark_tabs:', ':bar_chart:', ':chart_with_upwards_trend:', ':chart_with_downwards_trend:', ':scroll:', ':clipboard:',
          ':calendar:', ':date:', ':card_index:', ':file_folder:', ':open_file_folder:', ':scissors:', ':pushpin:', ':paperclip:',
          ':black_nib:', ':pencil2:', ':straight_ruler:', ':triangular_ruler:', ':closed_book:', ':green_book:', ':blue_book:',
          ':orange_book:', ':notebook:', ':notebook_with_decorative_cover:', ':ledger:', ':books:', ':bookmark:', ':name_badge:',
          ':microscope:', ':telescope:', ':newspaper:', ':football:', ':basketball:', ':soccer:', ':baseball:', ':tennis:', ':8ball:',
          ':rugby_football:', ':bowling:', ':golf:', ':gem:', ':ring:', ':trophy:', ':musical_score:', ':musical_keyboard:', ':violin:',
          ':video_game:', ':flower_playing_cards:', ':game_die:', ':dart:', ':clapper:', ':memo:', ':pencil:', ':book:', ':art:', ':microphone:',
          ':headphones:', ':trumpet:', ':saxophone:', ':guitar:', ':shoe:', ':sandal:', ':high_heel:', ':lipstick:', ':boot:', ':shirt:',
          ':tshirt:', ':necktie:', ':womans_clothes:', ':dress:', ':running_shirt_with_sash:', ':jeans:', ':kimono:', ':bikini:', ':ribbon:',
          ':tophat:', ':crown:', ':womans_hat:', ':mans_shoe:', ':closed_umbrella:', ':briefcase:', ':handbag:', ':pouch:', ':purse:',
          ':eyeglasses:', ':fishing_pole_and_fish:', ':coffee:', ':tea:', ':sake:', ':baby_bottle:', ':beer:', ':beers:', ':cocktail:',
          ':tropical_drink:', ':wine_glass:', ':fork_and_knife:', ':pizza:', ':hamburger:', ':fries:', ':poultry_leg:', ':meat_on_bone:',
          ':spaghetti:', ':curry:', ':fried_shrimp:', ':bento:', ':sushi:', ':fish_cake:', ':rice_ball:', ':rice_cracker:', ':rice:',
          ':ramen:', ':stew:', ':oden:', ':dango:', ':egg:', ':bread:', ':doughnut:', ':custard:', ':icecream:', ':ice_cream:', ':shaved_ice:',
          ':birthday:', ':cake:', ':cookie:', ':chocolate_bar:', ':candy:', ':lollipop:', ':honey_pot:', ':apple:', ':green_apple:',
          ':tangerine:', ':lemon:', ':cherries:', ':grapes:', ':watermelon:', ':strawberry:', ':peach:', ':melon:', ':banana:', ':pear:',
          ':pineapple:', ':sweet_potato:', ':eggplant:', ':tomato:', ':corn:', ':house:', ':house_with_garden:', ':school:', ':office:',
          ':post_office:', ':hospital:', ':bank:', ':convenience_store:', ':love_hotel:', ':hotel:', ':wedding:', ':church:', ':department_store:',
          ':european_post_office:', ':city_sunrise:', ':city_sunset:', ':japanese_castle:', ':european_castle:', ':tent:', ':factory:',
          ':tokyo_tower:', ':japan:', ':mount_fuji:', ':sunrise_over_mountains:', ':sunrise:', ':stars:', ':statue_of_liberty:', ':bridge_at_night:',
          ':carousel_horse:', ':rainbow:', ':ferris_wheel:', ':fountain:', ':roller_coaster:', ':ship:', ':speedboat:', ':boat:', ':sailboat:',
          ':rowboat:', ':anchor:', ':rocket:', ':airplane:', ':helicopter:', ':steam_locomotive:', ':tram:', ':mountain_railway:', ':bike:',
          ':aerial_tramway:', ':suspension_railway:', ':mountain_cableway:', ':tractor:', ':blue_car:', ':oncoming_automobile:', ':car:',
          ':red_car:', ':taxi:', ':oncoming_taxi:', ':articulated_lorry:', ':bus:', ':oncoming_bus:', ':rotating_light:', ':police_car:',
          ':oncoming_police_car:', ':fire_engine:', ':ambulance:', ':minibus:', ':truck:', ':train:', ':station:', ':train2:', ':bullettrain_front:',
          ':bullettrain_side:', ':light_rail:', ':monorail:', ':railway_car:', ':trolleybus:', ':ticket:', ':fuelpump:', ':vertical_traffic_light:',
          ':traffic_light:', ':warning:', ':construction:', ':beginner:', ':atm:', ':slot_machine:', ':busstop:', ':barber:', ':hotsprings:',
          ':checkered_flag:', ':crossed_flags:', ':izakaya_lantern:', ':moyai:', ':circus_tent:', ':performing_arts:', ':round_pushpin:',
          ':triangular_flag_on_post:', ':jp:', ':kr:', ':cn:', ':us:', ':fr:', ':es:', ':it:', ':ru:', ':gb:', ':uk:', ':de:', ':one:', ':two:',
          ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:', ':1234:', ':zero:', ':hash:', ':symbols:',
          ':arrow_backward:', ':arrow_down:', ':arrow_forward:', ':arrow_left:', ':capital_abcd:', ':abcd:', ':abc:', ':arrow_lower_left:',
          ':arrow_lower_right:', ':arrow_right:', ':arrow_up:', ':arrow_upper_left:', ':arrow_upper_right:', ':arrow_double_down:', ':arrow_double_up:',
          ':arrow_down_small:', ':arrow_heading_down:', ':arrow_heading_up:', ':leftwards_arrow_with_hook:', ':arrow_right_hook:', ':left_right_arrow:',
          ':arrow_up_down:', ':arrow_up_small:', ':arrows_clockwise:', ':arrows_counterclockwise:', ':rewind:', ':fast_forward:', ':information_source:',
          ':ok:', ':twisted_rightwards_arrows:', ':repeat:', ':repeat_one:', ':new:', ':top:', ':up:', ':cool:', ':free:', ':ng:', ':cinema:', ':koko:',
          ':signal_strength:', ':u5272:', ':u5408:', ':u55b6:', ':u6307:', ':u6708:', ':u6709:', ':u6e80:', ':u7121:', ':u7533:', ':u7a7a:', ':u7981:',
          ':sa:', ':restroom:', ':mens:', ':womens:', ':baby_symbol:', ':no_smoking:', ':parking:', ':wheelchair:', ':metro:', ':baggage_claim:',
          ':accept:', ':wc:', ':potable_water:', ':put_litter_in_its_place:', ':secret:', ':congratulations:', ':m:', ':passport_control:',
          ':left_luggage:', ':customs:', ':ideograph_advantage:', ':cl:', ':sos:', ':id:', ':no_entry_sign:', ':underage:', ':no_mobile_phones:',
          ':do_not_litter:', ':non-potable_water:', ':no_bicycles:', ':no_pedestrians:', ':children_crossing:', ':no_entry:', ':eight_spoked_asterisk:',
          ':sparkle:', ':eight_pointed_black_star:', ':heart_decoration:', ':vs:', ':vibration_mode:', ':mobile_phone_off:', ':chart:',
          ':currency_exchange:', ':aries:', ':taurus:', ':gemini:', ':cancer:', ':leo:', ':virgo:', ':libra:', ':scorpius:', ':sagittarius:',
          ':capricorn:', ':aquarius:', ':pisces:', ':ophiuchus:', ':six_pointed_star:', ':negative_squared_cross_mark:', ':a:', ':b:', ':ab:', ':o2:',
          ':diamond_shape_with_a_dot_inside:', ':recycle:', ':end:', ':back:', ':on:', ':soon:', ':clock1:', ':clock130:', ':clock10:', ':clock1030:',
          ':clock11:', ':clock1130:', ':clock12:', ':clock1230:', ':clock2:', ':clock230:', ':clock3:', ':clock330:', ':clock4:', ':clock430:',
          ':clock5:', ':clock530:', ':clock6:', ':clock630:', ':clock7:', ':clock730:', ':clock8:', ':clock830:', ':clock9:', ':clock930:',
          ':heavy_dollar_sign:', ':copyright:', ':registered:', ':tm:', ':x:', ':heavy_exclamation_mark:', ':bangbang:', ':interrobang:', ':o:',
          ':heavy_multiplication_x:', ':heavy_plus_sign:', ':heavy_minus_sign:', ':heavy_division_sign:', ':white_flower:', ':100:', ':heavy_check_mark:',
          ':ballot_box_with_check:', ':radio_button:', ':link:', ':curly_loop:', ':wavy_dash:', ':part_alternation_mark:', ':trident:',
          ':black_small_square:', ':white_small_square:', ':black_medium_small_square:', ':white_medium_small_square:', ':black_medium_square:',
          ':white_medium_square:', ':white_large_square:', ':white_check_mark:', ':black_square_button:', ':white_square_button:',
          ':black_circle:', ':white_circle:', ':red_circle:', ':large_blue_circle:', ':large_blue_diamond:', ':large_orange_diamond:',
          ':small_blue_diamond:', ':small_orange_diamond:', ':small_red_triangle:', ':small_red_triangle_down:']


class EmojiPattern(markdown.inlinepatterns.Pattern):

    def handleMatch(self, m):
        emoji = self.unescape(m.group(2))
        if emoji not in EMOJIS:
            return emoji
        url = '{0}{1}.png'.format(
            MARTOR_MARKDOWN_BASE_EMOJI_URL, emoji.replace(':', '')
        )
        if MARTOR_MARKDOWN_BASE_EMOJI_USE_STATIC is True:
            url = static(url)
        el = markdown.util.etree.Element('img')
        el.set('src', url)
        el.set('class', 'marked-emoji')
        el.text = markdown.util.AtomicString(emoji)
        return el


class EmojiExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        """ Setup `emoji_img` with EmojiPattern """
        md.inlinePatterns['emoji_img'] = EmojiPattern(EMOJI_RE, md)


def makeExtension(*args, **kwargs):
    return EmojiExtension(*args, **kwargs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
