import logging
import argparse
import distutils.util
import yaml


LOGGER = logging.getLogger(__name__)


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, **kwargs):
        super().__init__(add_help=False, **kwargs)
        self.add_argument('-c', '--config', required=True, help='set config filepath')
        self.arguments_added = False

    def _add_arguments_from_config(self, args):
        parsed, _ = self.parse_known_args(args=args)
        with open(parsed.config, 'r') as f:
            options = yaml.safe_load(f)

        if not self.arguments_added:
            for key, value in options.items():
                self._add_argument(key, value)
            self.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='show this help message and exit')
        self.arguments_added = True

        return options

    def _add_argument(self, key, value, prefix=None):
        if key.startswith('_'):
            return
        key = key if prefix is None else prefix + '-' + key
        if key in self._option_string_actions:
            LOGGER.error('%s already exist arguments', key)
        elif isinstance(value, dict):
            for k, v in value.items():
                self._add_argument(k, v, key)
        elif isinstance(value, list):
            if value:
                self.add_argument('--' + key, type=type(value[0]), nargs='*', default=value,
                                  help='set ' + type(value[0]).__name__ + ' list (default:' + str(value).replace('%', '%%') + ')')
            else:
                self.add_argument('--' + key, nargs='*', default=value, help='set list (default:' + str(value) + ')')
        elif isinstance(value, bool):
            self.add_argument('--' + key, type=distutils.util.strtobool, default=value,
                              help='set ' + type(value).__name__ + ' value (default:' + str(value).replace('%', '%%') + ')')
        else:
            self.add_argument('--' + key, type=type(value), default=value,
                              help='set ' + type(value).__name__ + ' value (default:' + str(value).replace('%', '%%') + ')')

    def _update(self, parents, options, parsed_args):
        for key, value in options.items():
            name = '_'.join(parents + [key])
            if name in parsed_args:
                options[key] = parsed_args.__dict__[name]
            elif isinstance(value, dict):
                self._update(parents + [key], options[key], parsed_args)


    def parse_args(self, args=None, namespace=None, return_dict=False):
        options = self._add_arguments_from_config(args)
        parsed_args = super().parse_args(args, namespace)
        if not return_dict:
            return parsed_args

        self._update([], options, parsed_args)
        return options
