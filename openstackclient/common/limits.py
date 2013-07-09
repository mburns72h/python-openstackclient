#   Copyright 2012-2013 OpenStack Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Limits Action Implementation"""

import itertools
import logging

from cliff import lister

from openstackclient.common import utils


class ShowLimits(lister.Lister):
    """Show compute and volume limits"""

    log = logging.getLogger(__name__ + '.ShowLimits')

    def get_parser(self, prog_name):
        parser = super(ShowLimits, self).get_parser(prog_name)
        type_group = parser.add_mutually_exclusive_group()
        type_group.add_argument(
            "--absolute",
            dest="is_absolute",
            action="store_true",
            default=False,
            help="Show absolute limits")
        type_group.add_argument(
            "--rate",
            dest="is_rate",
            action="store_true",
            default=False,
            help="Show rate limits")
        parser.add_argument(
            "--reserved",
            dest="is_reserved",
            action="store_true",
            default=False,
            help="Include reservations count [only valid with --absolute]")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)

        compute_client = self.app.client_manager.compute
        volume_client = self.app.client_manager.volume

        compute_limits = compute_client.limits.get(parsed_args.is_reserved)
        volume_limits = volume_client.limits.get()

        if parsed_args.is_absolute:
            compute_limits = compute_limits.absolute
            volume_limits = volume_limits.absolute
            columns = ["Name", "Value"]
            return (columns, (utils.get_item_properties(s, columns)
                    for s in itertools.chain(compute_limits, volume_limits)))

        elif parsed_args.is_rate:
            compute_limits = compute_limits.rate
            volume_limits = volume_limits.rate
            columns = ["Verb", "URI", "Value", "Remain", "Unit",
                       "Next Available"]
            return (columns, (utils.get_item_properties(s, columns)
                    for s in itertools.chain(compute_limits, volume_limits)))

        else:
            return ({}, {})
