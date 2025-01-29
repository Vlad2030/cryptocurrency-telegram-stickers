# I HATE PYTHON

import datetime

from PIL import Image, ImageDraw, ImageFont

import assets
import core.cache
import utils.images
import utils.prettier


class CryptoCurrencySticker:
    def __init__(
        self,
        symbol: str,
        name: str,
        image: Image,
        price: float,
        market_cap: float,
        price_change_percent: float,
        timestamp: datetime.datetime,
        extra_text: str = "",
        quote_symbol: str = "$",
        round_logo: bool = True,
        mode: str = "white",
    ) -> None:
        self.symbol = symbol
        self.name = name
        self.image = image
        self.price = price
        self.market_cap = market_cap
        self.price_change_percent = price_change_percent
        self.timestamp = timestamp
        self.extra_text = extra_text
        self.quote_symbol = quote_symbol
        self.round_logo = round_logo
        self.mode = mode

        # image
        self._image = None
        self._image_supersampling = Image.Resampling.HAMMING
        self._image_width = 512
        self._image_width_supersampled = (
            self._image_width * self._image_supersampling
        )
        self._image_height = 512
        self._image_height_supersampled = (
            self._image_height * self._image_supersampling
        )
        self._image_corner_radius = 50
        self._image_corner_radius_supersampled = (
            self._image_corner_radius * self._image_supersampling
        )
        self._image_format = "png"
        self._image_mode = "RGBA"
        self._image_background_color_rgba = (
            (255, 255, 255, 255)
            if self.mode == "white"
            else (0, 0, 0, 255)
            if self.mode == "black"
            else (128, 128, 128, 255)
        )
        self._image_transparent_color_rgba = (255, 255, 255, 0)
        self._image_semi_transparent_color_rgba = (
            self._image_background_color_rgba[0] // 2
            if self._image_background_color_rgba[0] >= 1
            else 128,
            self._image_background_color_rgba[1] // 2
            if self._image_background_color_rgba[1] >= 1
            else 128,
            self._image_background_color_rgba[2] // 2
            if self._image_background_color_rgba[2] >= 1
            else 128,
            255,
        )
        self._image_border_width = 8
        self._image_border_width_supersampled = (
            self._image_border_width * self._image_supersampling
        )
        self._image_border_color_rgba = (
            (0, 0, 0, 255)
            if self.mode == "white"
            else (255, 255, 255, 255)
            if self.mode == "black"
            else (123, 123, 123, 255)
        )
        self._image_font_path = assets.fonts_path + "Jersey15-Regular.ttf"
        self._image_font_color_rgba = (
            (0, 0, 0, 255)
            if self.mode == "white"
            else (255, 255, 255, 255)
            if self.mode == "black"
            else (128, 128, 128, 255)
        )
        self._image_font_red_color_rgba = (164, 0, 0, 255)
        self._image_font_green_color_rgba = (19, 164, 0, 255)

        # logo
        self._image_logo_position_x = 30
        self._image_logo_position_x_supersampled = (
            self._image_logo_position_x * self._image_supersampling
        )
        self._image_logo_position_y = 30
        self._image_logo_position_y_supersampled = (
            self._image_logo_position_y * self._image_supersampling
        )
        self._image_logo_width = 152
        self._image_logo_width_supersampled = (
            self._image_logo_width * self._image_supersampling
        )
        self._image_logo_height = 152
        self._image_logo_height_supersampled = (
            self._image_logo_height * self._image_supersampling
        )
        self._image_logo_image = self.image.resize(
            size=(
                self._image_logo_width_supersampled,
                self._image_logo_height_supersampled,
            ),
            resample=self._image_supersampling,
        )

        # symbol text
        self._image_symbol_position_x = 200
        self._image_symbol_position_x_supersampled = (
            self._image_symbol_position_x * self._image_supersampling
        )
        self._image_symbol_position_y = 35
        self._image_symbol_position_y_supersampled = (
            self._image_symbol_position_y * self._image_supersampling
        )
        self._image_symbol_font_size = 80
        self._image_symbol_font_size_supersampled = (
            self._image_symbol_font_size * self._image_supersampling
        )
        self._image_symbol_font = ImageFont.truetype(
            font=self._image_font_path,
            size=self._image_symbol_font_size_supersampled,
        )
        self._image_symbol_opacity = 100
        self._image_symbol_color_rgba = self._image_font_color_rgba
        self._image_symbol_text = f"${self.symbol}".upper()

        # name text
        self._image_name_position_x = 200
        self._image_name_position_x_supersampled = (
            self._image_name_position_x * self._image_supersampling
        )
        self._image_name_position_y = 110
        self._image_name_position_y_supersampled = (
            self._image_name_position_y * self._image_supersampling
        )
        self._image_name_font_size = 64
        self._image_name_font_size_supersampled = (
            self._image_name_font_size * self._image_supersampling
        )
        self._image_name_font = ImageFont.truetype(
            font=self._image_font_path,
            size=self._image_name_font_size_supersampled,
        )
        self._image_name_opacity = 100
        self._image_name_color_rgba = self._image_font_color_rgba
        self._image_name_text = utils.prettier.name(self.name.capitalize())

        # quote value text
        self._image_quote_value_position_x = 30
        self._image_quote_value_position_x_supersampled = (
            self._image_quote_value_position_x * self._image_supersampling
        )
        self._image_quote_value_position_y = 190
        self._image_quote_value_position_y_supersampled = (
            self._image_quote_value_position_y * self._image_supersampling
        )
        self._image_quote_value_font_size = 86
        self._image_quote_value_font_size_supersampled = (
            self._image_quote_value_font_size * self._image_supersampling
        )
        self._image_quote_value_font = ImageFont.truetype(
            font=self._image_font_path,
            size=self._image_quote_value_font_size_supersampled,
        )
        self._image_quote_value_opacity = 100
        self._image_quote_value_color_rgba = self._image_font_color_rgba
        self._image_quote_value_text = utils.prettier.price(
            value=self.price,
            quote_symbol=self.quote_symbol,
        )

        # price change percent text
        self._image_price_change_percent_position_x = (
            self._image_quote_value_position_x + (self._image_width // 2)
        )
        self._image_price_change_percent_position_x_supersampled = (
            self._image_price_change_percent_position_x
            * self._image_supersampling
        )
        self._image_price_change_percent_position_y = 200
        self._image_price_change_percent_position_y_supersampled = (
            self._image_price_change_percent_position_y
            * self._image_supersampling
        )
        self._image_price_change_percent_font_size = 64
        self._image_price_change_percent_font_size_supersampled = (
            self._image_price_change_percent_font_size
            * self._image_supersampling
        )
        self._image_price_change_percent_font = ImageFont.truetype(
            font=self._image_font_path,
            size=self._image_price_change_percent_font_size_supersampled,
        )
        self._image_price_change_percent_opacity = 100
        self._image_price_change_percent_color_rgba = (
            self._image_font_green_color_rgba
            if self.price_change_percent >= 0.00
            else self._image_font_red_color_rgba
        )
        self._image_price_change_percent_text = utils.prettier.change_percent(
            value=self.price_change_percent,
        )

        # mcap value text
        self._image_mcap_value_position_x = 30
        self._image_mcap_value_position_x_supersampled = (
            self._image_mcap_value_position_x * self._image_supersampling
        )
        self._image_mcap_value_position_y = 290
        self._image_mcap_value_position_y_supersampled = (
            self._image_mcap_value_position_y * self._image_supersampling
        )
        self._image_mcap_value_font_size = 64
        self._image_mcap_value_font_size_supersampled = (
            self._image_mcap_value_font_size * self._image_supersampling
        )
        self._image_mcap_value_font = ImageFont.truetype(
            font=self._image_font_path,
            size=self._image_mcap_value_font_size_supersampled,
        )
        self._image_mcap_value_opacity = 100
        self._image_mcap_value_color_rgba = self._image_font_color_rgba
        self._image_mcap_value_text = utils.prettier.market_cap(
            value=self.market_cap,
            quote_symbol=self.quote_symbol,
        )

        # mcap label text
        self._image_mcap_label_position_x = (
            self._image_mcap_value_position_x + (self._image_width // 3)
        )
        self._image_mcap_label_position_x_supersampled = (
            self._image_mcap_label_position_x * self._image_supersampling
        )
        self._image_mcap_label_position_y = 312
        self._image_mcap_label_position_y_supersampled = (
            self._image_mcap_label_position_y * self._image_supersampling
        )
        self._image_mcap_label_font_size = 36
        self._image_mcap_label_font_size_supersampled = (
            self._image_mcap_label_font_size * self._image_supersampling
        )
        self._image_mcap_label_font = ImageFont.truetype(
            font=self._image_font_path,
            size=self._image_mcap_label_font_size_supersampled,
        )
        self._image_mcap_label_opacity = 50
        self._image_mcap_label_color_rgba = (
            self._image_semi_transparent_color_rgba
        )
        self._image_mcap_label_text = "Mcap"

        # extra text
        self._image_extra_position_x = 30
        self._image_extra_position_x_supersampled = (
            self._image_extra_position_x * self._image_supersampling
        )
        self._image_extra_position_y = 380
        self._image_extra_position_y_supersampled = (
            self._image_extra_position_y * self._image_supersampling
        )
        self._image_extra_font_size = 48
        self._image_extra_font_size_supersampled = (
            self._image_extra_font_size * self._image_supersampling
        )
        self._image_extra_font = ImageFont.truetype(
            font=self._image_font_path,
            size=self._image_extra_font_size_supersampled,
        )
        self._image_extra_opacity = 100
        self._image_extra_color_rgba = self._image_font_color_rgba
        self._image_extra_text = self.extra_text

        # updated at text
        self._image_updated_at_position_x = 0
        self._image_updated_at_position_x_supersampled = (
            self._image_updated_at_position_x * self._image_supersampling
        )
        self._image_updated_at_position_y = 480
        self._image_updated_at_position_y_supersampled = (
            self._image_updated_at_position_y * self._image_supersampling
        )
        self._image_updated_at_font_size = 28
        self._image_updated_at_font_size_supersampled = (
            self._image_updated_at_font_size * self._image_supersampling
        )
        self._image_updated_at_font = ImageFont.truetype(
            font=self._image_font_path,
            size=self._image_updated_at_font_size_supersampled,
        )
        self._image_updated_at_opacity = 50
        self._image_updated_at_color_rgba = (
            self._image_semi_transparent_color_rgba
        )
        self._image_updated_at_text = (
            f"Updated at {utils.prettier.timestamp(self.timestamp)}"
        )

    def generate(self) -> Image:
        self._image = Image.new(
            mode=self._image_mode,
            size=(
                self._image_width_supersampled,
                self._image_height_supersampled,
            ),
            color=self._image_transparent_color_rgba,
        )
        main_mask = Image.new(
            mode="L",
            size=(
                self._image_width_supersampled,
                self._image_height_supersampled,
            ),
            color=0,
        )

        draw = ImageDraw.Draw(main_mask)
        draw.rounded_rectangle(
            xy=(
                0,
                0,
                self._image_width_supersampled,
                self._image_height_supersampled,
            ),
            radius=self._image_corner_radius_supersampled,
            fill=255,
        )

        white_image = Image.new(
            mode=self._image_mode,
            size=(
                self._image_width_supersampled,
                self._image_height_supersampled,
            ),
            color=self._image_background_color_rgba,
        )

        self._image = Image.composite(
            image1=white_image,
            image2=self._image,
            mask=main_mask,
        )

        # logo
        if self.round_logo:
            logo_mask = Image.new(
                mode="L",
                size=(
                    self._image_logo_width_supersampled,
                    self._image_logo_height_supersampled,
                ),
                color=0,
            )
            logo_draw = ImageDraw.Draw(logo_mask)
            logo_draw.ellipse(
                xy=(
                    0,
                    0,
                    self._image_logo_width_supersampled,
                    self._image_logo_height_supersampled,
                ),
                fill=255,
            )
            self._image_logo_image = self._image_logo_image
            # self._image_logo_image = self._image_logo_image.copy()
            self._image_logo_image.putalpha(logo_mask)

        self._image.paste(
            im=self._image_logo_image,
            box=(
                self._image_logo_position_x_supersampled,
                self._image_logo_position_y_supersampled,
            ),
            mask=(logo_mask if self.round_logo else self._image_logo_image),
        )

        draw = ImageDraw.Draw(im=self._image)

        # symbol text
        (
            symbol_bbox_x1,
            symbol_bbox_y1,
            symbol_bbox_x2,
            symbol_bbox_y2,
        ) = draw.textbbox(
            xy=(
                self._image_symbol_position_x_supersampled,
                self._image_symbol_position_y_supersampled,
            ),
            text=self._image_symbol_text,
            font=self._image_symbol_font,
        )
        draw.text(
            xy=(
                self._image_symbol_position_x_supersampled,
                (
                    self._image_symbol_position_y_supersampled
                    - ((symbol_bbox_y2 - symbol_bbox_y2) // 2)
                ),
                # self._image_symbol_position_y_supersampled,
            ),
            text=self._image_symbol_text,
            font=self._image_symbol_font,
            fill=self._image_symbol_color_rgba,
        )

        # name text
        (
            name_bbox_x1,
            name_bbox_y1,
            name_bbox_x2,
            name_bbox_y2,
        ) = draw.textbbox(
            xy=(
                self._image_name_position_x_supersampled,
                self._image_name_position_y_supersampled,
            ),
            text=self._image_name_text,
            font=self._image_name_font,
        )
        draw.text(
            xy=(
                self._image_name_position_x_supersampled,
                (
                    self._image_name_position_y_supersampled
                    - ((name_bbox_y2 - name_bbox_y2) // 2)
                ),
                # self._image_name_position_y_supersampled,
            ),
            text=self._image_name_text,
            font=self._image_name_font,
            fill=self._image_name_color_rgba,
        )

        # quote value text
        (
            quote_value_bbox_x1,
            quote_value_bbox_y1,
            quote_value_bbox_x2,
            quote_value_bbox_y2,
        ) = draw.textbbox(
            xy=(
                self._image_quote_value_position_x_supersampled,
                self._image_quote_value_position_y_supersampled,
            ),
            text=self._image_quote_value_text,
            font=self._image_quote_value_font,
        )
        draw.text(
            xy=(
                self._image_quote_value_position_x_supersampled,
                self._image_quote_value_position_y_supersampled,
                # (
                #     self._image_quote_value_position_y_supersampled
                #     + ((text_bbox_y2 - text_bbox_y1) // 2)
                # ),
            ),
            text=self._image_quote_value_text,
            font=self._image_quote_value_font,
            fill=self._image_quote_value_color_rgba,
        )

        # percent change value text
        (
            price_change_percent_value_bbox_x1,
            price_change_percent_value_bbox_y1,
            price_change_percent_value_bbox_x2,
            price_change_percent_value_bbox_y2,
        ) = draw.textbbox(
            xy=(
                self._image_price_change_percent_position_x_supersampled,
                self._image_price_change_percent_position_y_supersampled,
            ),
            text=self._image_price_change_percent_text,
            font=self._image_price_change_percent_font,
        )
        draw.text(
            xy=(
                (quote_value_bbox_x2 + 0),  # + 10
                # self._image_price_change_percent_position_x_supersampled,
                self._image_price_change_percent_position_y_supersampled,
            ),
            text=self._image_price_change_percent_text,
            font=self._image_price_change_percent_font,
            fill=self._image_price_change_percent_color_rgba,
        )

        # mcap value text
        (
            mcap_value_value_bbox_x1,
            mcap_value_value_bbox_y1,
            mcap_value_value_bbox_x2,
            mcap_value_value_bbox_y2,
        ) = draw.textbbox(
            xy=(
                self._image_mcap_value_position_x_supersampled,
                self._image_mcap_value_position_y_supersampled,
            ),
            text=self._image_mcap_value_text,
            font=self._image_mcap_value_font,
        )
        draw.text(
            xy=(
                self._image_mcap_value_position_x_supersampled,
                self._image_mcap_value_position_y_supersampled,
            ),
            text=self._image_mcap_value_text,
            font=self._image_mcap_value_font,
            fill=self._image_mcap_value_color_rgba,
        )

        # mcap label text
        (
            mcap_label_value_bbox_x1,
            mcap_label_value_bbox_y1,
            mcap_label_value_bbox_x2,
            mcap_label_value_bbox_y2,
        ) = draw.textbbox(
            xy=(
                self._image_mcap_label_position_x_supersampled,
                self._image_mcap_label_position_y_supersampled,
            ),
            text=self._image_mcap_label_text,
            font=self._image_mcap_label_font,
        )
        draw.text(
            xy=(
                (mcap_value_value_bbox_x2 + 20),
                # self._image_mcap_label_position_x_supersampled,
                self._image_mcap_label_position_y_supersampled,
            ),
            text=self._image_mcap_label_text,
            font=self._image_mcap_label_font,
            fill=self._image_mcap_label_color_rgba,
        )

        # extra text
        (
            extra_bbox_x1,
            extra_bbox_y1,
            extra_bbox_x2,
            extra_bbox_y2,
        ) = draw.textbbox(
            xy=(
                self._image_extra_position_x_supersampled,
                self._image_extra_position_y_supersampled,
            ),
            text=self._image_extra_text,
            font=self._image_extra_font,
        )
        draw.text(
            xy=(
                self._image_extra_position_x_supersampled,
                self._image_extra_position_y_supersampled,
            ),
            text=self._image_extra_text,
            font=self._image_extra_font,
            fill=self._image_extra_color_rgba,
        )

        # updated at text
        (
            updated_at_bbox_x1,
            updated_at_bbox_y1,
            updated_at_bbox_x2,
            updated_at_bbox_y2,
        ) = draw.textbbox(
            xy=(
                self._image_updated_at_position_x_supersampled,
                self._image_updated_at_position_y_supersampled,
            ),
            text=self._image_updated_at_text,
            font=self._image_updated_at_font,
        )
        draw.text(
            xy=(
                ((self._image_width_supersampled - (updated_at_bbox_x2)) // 2),
                # self._image_updated_at_position_x_supersampled,
                self._image_updated_at_position_y_supersampled,
            ),
            text=self._image_updated_at_text,
            font=self._image_updated_at_font,
            fill=self._image_updated_at_color_rgba,
        )

        self._image = self._image.resize(
            size=(self._image_width, self._image_height),
            resample=self._image_supersampling,
            reducing_gap=10.00,
        )

        return self._image


def process_render(data: dict) -> None:
    logo = core.cache.cached_logo.get(data["symbol"])

    if logo is None:
        return None

    ccs = CryptoCurrencySticker(
        symbol=data["symbol"],
        name=data["name"],
        image=utils.images.from_base64(logo),
        price=data["price"],
        market_cap=data["market_cap"],
        price_change_percent=data["price_change_percent"],
        timestamp=data["timestamp"],
        extra_text=data["extra_text"],
        round_logo=data["round_logo"],
        mode=data["mode"],
    )

    image = ccs.generate()

    core.logging.logger.info(f"Rendered {data["symbol"]} sticker")

    image.save(f"{assets.images_stickers_path}{data["count"]}.png", "PNG")

    core.logging.logger.info(
        f"Saved into {assets.images_stickers_path}{data["count"]}.png"
    )
