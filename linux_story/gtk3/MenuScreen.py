#!/usr/bin/env python

# menu_screen.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Shows the menu for selecting the appropriate challenge

import os
from gi.repository import Gtk, GObject

from linux_story.common import get_max_challenge_number
from kano.gtk3.buttons import KanoButton
from kano_profile.apps import load_app_state_variable


# This doesn't include the introduction as the introduction isn't a challenge
chapters = {
    1: {
        'start_challenge': 1,
        'end_challenge': 9,
        'title': 'Start exploring'
    },
    2: {
        'start_challenge': 10,
        'end_challenge': 16,
        'title': 'Save a family'
    },
    3: {
        'start_challenge': 17,
        'end_challenge': 22,
        'title': 'Go to the farm'
    }
}


# Contains the text describing the challenges
challenges = {
    1: {
        'title': 'Wake up!',
        'chapter': 1
    },
    2: {
        'title': 'Look in your wardrobe',
        'chapter': 1
    },
    3: {
        'title': 'Look on your shelves',
        'chapter': 1
    },
    4: {
        'title': 'Find Mum',
        'chapter': 1
    },
    5: {
        'title': 'Where\'s Dad?',
        'chapter': 1
    },
    6: {
        'title': 'Visit the town',
        'chapter': 1
    },
    7: {
        'title': 'Town meeting',
        'chapter': 1
    },
    8: {
        'title': 'The bell strikes',
        'chapter': 1
    },
    9: {
        'title': 'Where\'s Mum?',
        'chapter': 1
    },
    10: {
        'title': 'See more clearly',
        'chapter': 2
    },
    11: {
        'title': 'Save the girl',
        'chapter': 2
    },
    12: {
        'title': 'Save the dog',
        'chapter': 2
    },
    13: {
        'title': 'Food hunt',
        'chapter': 2
    },
    14: {
        'title': 'Folderton Hero',
        'chapter': 2
    },
    15: {
        'title': 'Have a closer look',
        'chapter': 2
    },
    16: {
        'title': 'A gift',
        'chapter': 2
    },
    17: {
        'title': '',
        'chapter': 3
    },
    18: {
        'title': '',
        'chapter': 3
    },
    19: {
        'title': '',
        'chapter': 3
    },
    20: {
        'title': '',
        'chapter': 3
    },
    21: {
        'title': '',
        'chapter': 3
    },
    22: {
        'title': '',
        'chapter': 3
    },
    23: {
        'title': '',
        'chapter': 3
    }
}


class MenuScreen(Gtk.EventBox):
    '''This shows the user the challenges they can select.
    '''

    __gsignals__ = {
        # This returns an integer of the challenge the user wants to start from
        'challenge_selected': (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }

    def __init__(self):
        Gtk.EventBox.__init__(self)

        # Find the greatest challenge that has been created according to
        # kano profile
        self.max_challenge = get_max_challenge_number()

        # Get the last unlocked challenge.
        self.last_unlocked_challenge = load_app_state_variable('linux-story', 'level')

        # With this data, we need to decide which chapters are locked.
        self.last_unlocked_chapter = challenges[self.last_unlocked_challenge]['chapter']

        menu = self.continue_story_or_select_chapter_menu()
        self.add(menu)

    def continue_story_or_select_chapter_menu(self):
        '''This gives the user a simple option of just continuing the story
        from where they left off, or selecting the chapter manually
        '''
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # This takes the user to the latest point in the story
        continue_btn = KanoButton("CONTINUE")
        continue_btn.connect(
            'clicked', self.launch_challenge, self.last_unlocked_challenge
        )

        # This takes the user to the chapter menu
        select_chapter_btn = KanoButton('SELECT CHAPTER')
        select_chapter_btn.connect('clicked', self.show_chapter_menu_wrapper)

        vbox.pack_start(continue_btn, False, False, 0)
        vbox.pack_start(select_chapter_btn, False, False, 0)

        return vbox

    ################################################################
    # Lots of repetition here.

    def show_challenge_menu_wrapper(self, widget, challenge_number):
        self.show_challenge_menu(challenge_number)

    def show_challenge_menu(self, challenge_number):
        '''Show a menu for the challenges available in a certain chapter
        '''
        for child in self.get_children():
            self.remove(child)

        grid = self.create_challenge_menu(challenge_number)
        self.add(grid)
        self.show_all()

    def show_chapter_menu_wrapper(self, widget):
        self.show_chapter_menu()

    def show_chapter_menu(self):
        for child in self.get_children():
            self.remove(child)

        grid = self.create_chapter_menu()
        self.add(grid)
        self.show_all()

    def create_chapter_menu(self):
        '''Create a menu of the available chapters
        '''
        grid = Gtk.Grid()
        num_of_chapters = len(chapters)

        row = 0
        column = 0
        total_columns = 6

        for i in range(1, num_of_chapters + 1):
            button = self.create_chapter_button(i)
            grid.attach(button, column, row, 1, 1)
            column += 1

            if column > total_columns:
                row += 1
                column = 0

        return grid

    def create_challenge_menu(self, chapter_number):
        grid = Gtk.Grid()
        start_challenge = chapters[chapter_number]['start_challenge']
        end_challenge = chapters[chapter_number]['end_challenge']

        row = 0
        column = 0
        total_columns = 6

        for i in range(start_challenge, end_challenge + 1):
            button = self.create_challenge_button(i)
            grid.attach(button, column, row, 1, 1)
            column += 1

            if column > total_columns:
                row += 1
                column = 0

        return grid

    def create_challenge_button(self, challenge_number):
        button = KanoButton(challenge_number)
        button.connect("clicked", self.launch_challenge, challenge_number)

        title = challenges[challenge_number]['title']
        button.set_property('has-tooltip', True)
        button.connect('query-tooltip', self.custom_tooltip, title)

        # If the chapter number is greater than the maximum chapter unlocked,
        # set the styling to locked and make it insensitive.
        if challenge_number > self.last_unlocked_challenge:
            button.get_style_context().add_class("locked")
            button.set_sensitive(False)

        return button

    def custom_tooltip(self, x, y, z, a, tooltip, title):
        '''There is a much simpler function for having a tooltip with just
        text, but if we want to make it more complex, we can just modify this
        widget here.
        '''
        # Edit this if we want the tooltip to get any more complicated.
        custom_widget = Gtk.Label(title)
        tooltip.set_custom(custom_widget)
        return True

    def create_chapter_button(self, chapter_number):
        button = KanoButton(chapter_number)
        button.connect(
            "clicked", self.show_challenge_menu_wrapper, chapter_number
        )
        # If the chapter number is greater than the maximum chapter unlocked,
        # set the styling to locked and make it insensitive.
        if chapter_number > self.last_unlocked_chapter:
            button.get_style_context().add_class("locked")
            button.set_sensitive(False)

        return button

    ####################################################################

    def launch_challenge(self, widget, challenge_number):
        self.emit('challenge_selected', challenge_number)

    # Currently not used, as linux-story-gui should have been launched by the
    # time you inialise this class.
    def directly_launch_challenge(self, challenge_number):
        # We want to launch either the local linux-story-gui or the system one,
        # depending on where this file is.
        # If this starts with /usr/ go to /usr/bin, otherwise use a relative
        # path.
        if os.path.dirname(__file__).startswith('/usr'):
            filepath = '/usr/bin/linux-story-gui'
        else:
            filepath = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "../../bin/linux-story-gui"
                )
            )

        command = (
            "python " +
            filepath + " " +
            str(challenge_number) + " 1"
        )

        os.system(command)


class TestWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.connect('delete-event', Gtk.main_quit)
        menu = MenuScreen()
        self.add(menu)
        self.show_all()


if __name__ == '__main__':
    TestWindow()
    Gtk.main()
