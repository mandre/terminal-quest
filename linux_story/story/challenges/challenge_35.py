#!/usr/bin/env python
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_commands_with_cd_hint
from linux_story.story.challenges.challenge_36 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 35


class Step1(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Your name is written in this world, for anyone who knows where to look. Use}} {{yb:ls -l}} "
        "to see what I mean.}}"
    ]
    commands = [
        "ls -l"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Do you see your name on the files? You have extra abilities in this world, and the best "
        "chance of stopping this thing.}}",
        "{{Bb:I will teach you how to unlock the private section.}}",
        "{{Bb:Look around.}}"
    ]
    commands = ["ls"]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Go into the basement you see.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = ["cd basement"]

    def check_command(self):
        if self.last_user_input.strip() in self.commands:
            print "-bash: cd: basement: Permission denied"
            return True
        else:
            self.send_hint("{{rb:Use}} {{yb:cd basement/}} {{rb:to go into the basement.}}")
            return False

    def block_command(self):
        if self.last_user_input.startswith("cd"):
            return True

    def next(self):
        Step4()


# Make directory executable
class Step4(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:You got the error}} {{yb:-bash: cd: basement: Permission denied}}",
        "{{Bb:Normally you can do 3 things to a directory.}}",
        "",
        "{{Bb:See what is inside -}} {{lb:read}}",
        "{{Bb:Create something inside -}} {{lb:write}}",
        "{{Bb:Go inside with cd -}} {{lb:execute}}",
        "",
        "{{Bb:This directory is missing all three.}}"
        "",
        "{{Bb:To go inside, you need to activate the execute one.}}",
        "{{Bb:Use}} {{yb:chmod +x basement}} {{Bb:to unlock the basement.}}"
    ]
    commands = [
        "chmod +x basement",
        "chmod +x basement/"
    ]
    hints = [
        "{{rb:Use}} {{yb:chmod +x basement/}} {{rb:to unlock the basement.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

    def next(self):
        NextStep()
