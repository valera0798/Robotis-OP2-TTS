from base import InterfaceTTSClient, LoggableInterface
from errno import EEXIST


class AbstractTTSClient(InterfaceTTSClient, LoggableInterface):
    """
    Abstract TTS client class.
        - Declares abstract structure of TTS client.
        - Behaves like TTS client.
        - Should be used as parent of all TTS clients.
        - Supports logging feature.
    """
    _config_tts = None               # configuration of specific TTS client
    _str_path_output_dir = None      # audio output directory
    _str_format_file_audio = None    # audio file format

    def __init__(self, dict_config):
        """
        Constructs instance of AbstractTTSClient class.

        :param dict_config: configuration of TTS client.
        """
        super(AbstractTTSClient, self).__init__(name=self.__class__.__name__)
        self.set_configuration(dict_config)
        self.logger.debug("Instance initialization succeeds.")

    def set_configuration(self, dict_config):
        """
        Sets configuration of client instance.

        :param dict_config: dict - configuration of TTS client.
        :return: None (fields will be initialized).
        """
        if self.validate_configuration(dict_config):
            from os import makedirs
            from os.path import abspath

            self._str_format_file_audio = dict_config['audio_file_format'].encode('ascii', 'ignore')      # audio file format configuration
            dict_config.pop('audio_file_format', None)                          # to not to duplicate data
            self._config_tts = dict_config

            self._str_path_output_dir = abspath(self._str_path_output_dir)      # creates audio output directory
            try:
                makedirs(self._str_path_output_dir)
                self.logger.debug("Output audio directory is created. Output directory path = %s",
                                  self._str_path_output_dir)
            except OSError or EEXIST:
                self.logger.debug("Output audio directory is already exists. Output directory path = %s",
                                  self._str_path_output_dir)
                pass

    def _get_path_file_audio(self, source_text):
        """
        Returns path to audio file with source_text pronounced.

        :param source_text: source text to synthesize speech.
        :return: str - path to audio file.
        """
        from io import TextIOBase
        from os.path import basename, join

        # creates audio file corresponding to source text
        if isinstance(source_text, TextIOBase):             # if source_text is represented as file
            _str_name_file_audio = basename(source_text.name).split(".")[0]
        else:                                               # if source_text is represented as string
            if len(source_text) < 10:
                _str_name_file_audio = source_text          # full string
            else:
                _str_name_file_audio = source_text[:10]     # first 10 character from string
        _str_name_file_audio = "%s.%s" % (_str_name_file_audio, self._str_format_file_audio)
        str_path_file_audio = join(self._str_path_output_dir, _str_name_file_audio)
        self.logger.debug("Audio file path = %s", str_path_file_audio)
        return str_path_file_audio


class AbstractTTSClientDelegate(InterfaceTTSClient, LoggableInterface):
    """
    Abstract TTS client delegate class.
        - Declares abstract structure of TTS client delegates.
        - Behaves like TTS client.
        - Should be used as parent of all TTS client delegates.
        - Supports logging feature.
    """
    _config_tts = None              # configuration of specific TTS client
    _client_tts = None              # specific TTS client
    _str_command_play_audio = None  # command to call audio player

    def __init__(self, dict_config):
        """
        Constructs instance of AbstractTTSClientDelegate class.

        :param dict_config: configuration of TTS client.
        """
        super(AbstractTTSClientDelegate, self).__init__(name=self.__class__.__name__)
        self.set_configuration(dict_config)
        self.logger.debug("Instance initialization succeeds.")

    def set_configuration(self, dict_config):
        """
        Sets configuration of delegate instance.
            - Sets input configuration as _config_tts field.

        * Validates passed configuration before set.

        :param dict_config: dict - configuration of TTS client.
        :return: None (fields will be initialized).
        """
        if self.validate_configuration(dict_config):
            self._str_command_play_audio = dict_config['audio_file_player']['command'].encode('ascii', 'ignore')
            dict_config.pop('audio_file_player')    # to not to duplicate data
            self._config_tts = dict_config