# Lemonade stand is Licensed under the Don't Be A Dick License
# (dbad-license). This license is an extension of the Apache License.
#
# You may find a copy of this license at http://dbad-license.org/license
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Authors:
#     Justin Lewis <jlew.blackout@gmail.com>
#     Nathaniel Case <Qalthos@gmail.com>

from fortuneengine.GameEngineElement import GameEngineElement
from constants import ITEMS
from gettext import gettext as _
from pygame import font, Surface
from pygame.locals import KEYDOWN, K_RETURN, K_BACKSPACE, K_TAB ,K_DOWN, K_UP


class LemonadeGui(GameEngineElement):
    def __init__(self):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)
        self.__font = font.SysFont("Arial", 15)
        self.add_to_engine()

        self.__input_keys = ITEMS.keys()
        self.__input_mode = 0
        self.__input_string = ['0'] * len(self.__input_keys)

    def draw(self, screen, tick):
        main = self.game_engine.get_object('main')

        screen.fill((0, 0, 255))

        text_array = []

        # Corner Data Block
        myfont = font.SysFont(font.get_default_font(), 16)
        text_array.append( _("Day: %d") % main.day)
        text_array.append( _("Weather: %s") % "TODO")

        i = 10
        for text in text_array:
            ren = myfont.render( text, True, (255,255,255))
            screen.blit(ren, (10,i))
            i += ren.get_height()

        # REST TODO
        text_array = []
        text_array.append( _("Money: %d") % main.money )
        items = main.resource_list
        for item_key in items:
            text_array.append( "%s: %d" % (ITEMS[item_key]['name'], items[item_key]) )

        for message in main.messages:
            text_array.append( message )

        text_array.append("")
        text_array.append("buy")

        for i in range(0, len(self.__input_keys)):
            if i == self.__input_mode:
                t = ">"

            else:
                t = " "

            text_array.append("%s %s(%d@$%d): %s" % \
                (t, ITEMS[self.__input_keys[i]]['name'],
                 ITEMS[self.__input_keys[i]]['bulk'],
                 ITEMS[self.__input_keys[i]]['cost'],
                 self.__input_string[i] ))

        i = 0
        for text in text_array:
            ren = self.__font.render( text, True, (255,255,255))

            screen.blit(ren, (100,i))
            i += ren.get_height()

    def event_handler(self, event):
        if event.type == KEYDOWN:

            if event.key == K_RETURN:
                # Process Data

                item_list = {}
                for i in range(0, len(self.__input_keys)):
                    item_list[self.__input_keys[i]] = \
                                int(self.__input_string[i])
                    self.__input_string[i] = "0"
                main = self.game_engine.get_object('main')
                main.process_day_logic( item_list )


            elif event.key == K_BACKSPACE:
                handle = self.__input_string[self.__input_mode]

                if len(handle) == 1:
                    handle = "0"
                else:
                    handle = handle[0:-1]

                self.__input_string[self.__input_mode] = handle

            # Go to the next field
            elif event.key in [K_TAB, K_DOWN]:
                self.__input_mode = \
                    (self.__input_mode + 1) % len( self.__input_keys )

            # Go up to previous field
            elif event.key == K_UP:
                self.__input_mode = \
                    (self.__input_mode - 1) % len( self.__input_keys )

            # Only handle numbers (ascii 48 - 58)
            elif event.key >= 48 and event.key <= 58:
                key = str(event.unicode)

                handle = self.__input_string[self.__input_mode]

                if handle == "0":
                    handle = key
                else:
                    handle = "%s%s" % (handle, key)

                self.__input_string[self.__input_mode] = handle

            self.game_engine.set_dirty()
