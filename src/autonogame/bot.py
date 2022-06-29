#!/usr/bin/env python3

import logging
import time
import traceback

from ogame import OGame
from ogame.constants import buildings

logging.getLogger(__name__)
logging.root.setLevel(logging.INFO)


class OgameBot(object):

    stop_command = False
    logout_command = False
    running = False
    # TODO add it to settings
    refresh_time = 10  # seconds

    # deposit capacity in k starting from level 0
    DEPOSIT_CAPACITY = [
        10,
        20,
        40,
        75,
        140,
        255,
        470,
        865,
        1590,
        2920,
        5355,
        9820,
        18005,
        33005,
        60510,
        110925,
    ]

    # Initial build steps based on
    # https://ogame.fandom.com/wiki/Quick_Start_Guide
    EARLY_STAGE_STEPS = [
        # (building, level)
        (buildings.solar_plant, 1),
        (buildings.metal_mine, 1),
        (buildings.metal_mine, 2),
        (buildings.solar_plant, 2),
        (buildings.metal_mine, 3),
        (buildings.metal_mine, 4),
        (buildings.solar_plant, 3),
        (buildings.crystal_mine, 1),
        (buildings.solar_plant, 4),
        (buildings.metal_mine, 5),
        (buildings.crystal_mine, 2),
        (buildings.crystal_mine, 3),
        (buildings.solar_plant, 5),
        (buildings.deuterium_mine, 1),
        (buildings.crystal_mine, 4),
        (buildings.solar_plant, 6),
        (buildings.metal_mine, 6),
        (buildings.metal_mine, 7),
        (buildings.solar_plant, 7),
        (buildings.crystal_mine, 5),
        (buildings.deuterium_mine, 2),
        (buildings.solar_plant, 8),
        (buildings.deuterium_mine, 3),
        (buildings.deuterium_mine, 4),
        (buildings.solar_plant, 9),
        (buildings.deuterium_mine, 5),
        (buildings.robotics_factory, 1),
        (buildings.robotics_factory, 2),
        (buildings.research_laboratory, 1),
        (buildings.shipyard, 1),
        (buildings.crystal_mine, 6),
        (buildings.shipyard, 2),
        (buildings.solar_plant, 10),
        (buildings.deuterium_mine, 6),
        (buildings.metal_mine, 8),
        # research: energy technology
        # research: combustion drive
        (buildings.solar_plant, 11),
        (buildings.crystal_mine, 7),
        (buildings.metal_mine, 9),
    ]

    def __init__(self, empire: OGame):
        self.empire = empire
        self.planet_ids = self.empire.planet_ids()

    def attach_observer(self, notify):
        self.notify = notify

    def build_deposits(self, planet_id):
        if self.stop_command:
            return

        self.notify("build_deposits...")

        self.notify(
            f"Deposits: {self.metal_storage.level} "
            + f" {self.crystal_storage.level} "
            + f" {self.deuterium_storage.level}"
        )

        # upgrade deposit if it is at 90% of its capacity or above
        if (self.curr_planet_res.metal * 100) / (
            self.DEPOSIT_CAPACITY[self.metal_storage.level] * 1000
        ) > 90:
            if self.metal_storage.is_possible:
                self.notify("Building metal_storage")
                self.empire.build(what=buildings.metal_storage, id=planet_id)

        if (self.curr_planet_res.crystal * 100) / (
            self.DEPOSIT_CAPACITY[self.crystal_storage.level] * 1000
        ) > 90:
            if self.crystal_storage.is_possible:
                self.notify("Building crystal_storage")
                self.empire.build(what=buildings.crystal_storage, id=planet_id)

        if (self.curr_planet_res.deuterium * 100) / (
            self.DEPOSIT_CAPACITY[self.deuterium_storage.level] * 1000
        ) > 90:
            if self.deuterium_storage.is_possible:
                self.notify("Building deuterium_storage")
                self.empire.build(
                    what=buildings.deuterium_storage, id=planet_id
                )

    def build_mines(self, planet_id):
        if self.stop_command:
            return

        self.notify("build_mines...")

        self.notify(
            f"Mines: {self.metal_mine.level} "
            + f"{self.crystal_mine.level} "
            + f"{self.deuterium_mine.level} {self.solar_plant.level}"
        )

        if self.curr_planet_res.energy <= 0:
            self.notify("Energy is lower or equal than 0!")
            if self.solar_plant.is_possible:
                self.notify("Building solar_plant")
                self.empire.build(what=buildings.solar_plant, id=planet_id)
            return

        # Strategy
        # 1) Check: level of metal mine must be 2 levels higher
        #           than crystal mine.
        # 2) Check: for every 2 levels of crystal mines 1 level of
        #           deuterium mine must be built.
        # 3) Upgrade metal mine
        if self.crystal_mine.level < self.metal_mine.level - 2:
            if self.crystal_mine.is_possible:
                self.notify("Building crystal_mine")
                self.empire.build(what=buildings.crystal_mine, id=planet_id)
            return
        if self.deuterium_mine.level < self.crystal_mine.level // 2:
            if self.deuterium_mine.is_possible:
                self.notify("Building deuterium_mine")
                self.empire.build(what=buildings.deuterium_mine, id=planet_id)
            return
        if self.metal_mine.is_possible:
            self.notify("Building metal_mine")
            self.empire.build(what=buildings.metal_mine, id=planet_id)
            return

    def start(self):
        self.stop_command = False
        if self.running:
            self.notify("The bot is already running")
            return
        self.running = True
        self.notify("Started")

        while not self.stop_command:
            for planet_id in self.planet_ids:
                if self.stop_command:
                    break
                try:
                    self.update_current_planet_info(planet_id)

                    # Early stage strategy
                    early_stage_planet = False
                    for step_tuple, level in self.EARLY_STAGE_STEPS:
                        if step_tuple[2] == "supplies":
                            structures = self.curr_planet_sup
                        if step_tuple[2] == "facilities":
                            structures = self.curr_planet_fac
                        if structures:
                            if (
                                getattr(
                                    structures,
                                    buildings.building_name(step_tuple),
                                ).level
                                < level
                            ):
                                early_stage_planet = True
                                if getattr(
                                    structures,
                                    buildings.building_name(step_tuple),
                                ).is_possible:
                                    self.notify(
                                        "Building "
                                        + buildings.building_name(step_tuple)
                                        + " lv. "
                                        + str(level)
                                        + " on planet "
                                        + self.current_planet_name
                                    )
                                    self.empire.build(
                                        what=step_tuple, id=planet_id
                                    )
                                break

                    if not early_stage_planet:
                        # Not early stage planet strategy
                        self.build_deposits(planet_id)
                        self.build_mines(planet_id)

                except Exception:
                    logging.error(traceback.print_exc())
                    self.refresh_session()
                finally:
                    self.notify(f"Updating in {self.refresh_time}s...")
                    time.sleep(self.refresh_time)
        self.running = False
        self.stop_command = False
        self.notify("Stopped")

    def refresh_session(self):
        self.notify("Refreshing session...")
        self.empire.relogin()
        self.planet_ids = self.empire.planet_ids()

    def stop(self):
        self.stop_command = True

    def logout(self):
        self.logout_command = True

    def update_current_planet_info(self, planet_id):
        # get planet name
        self.current_planet_name = self.empire.name_by_planet_id(planet_id)
        # get resources, supplies and facilities
        self.curr_planet_res = self.empire.resources(planet_id)
        self.curr_planet_sup = self.empire.supply(planet_id)
        self.curr_planet_fac = self.empire.facilities(planet_id)
        # update resources
        self.metal_mine = self.curr_planet_sup.metal_mine
        self.crystal_mine = self.curr_planet_sup.crystal_mine
        self.deuterium_mine = self.curr_planet_sup.deuterium_mine
        self.solar_plant = self.curr_planet_sup.solar_plant
        # update deposits
        self.metal_storage = self.curr_planet_sup.metal_storage
        self.crystal_storage = self.curr_planet_sup.crystal_storage
        self.deuterium_storage = self.curr_planet_sup.deuterium_storage
