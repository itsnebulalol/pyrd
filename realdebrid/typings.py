from typing import TypedDict, List, NotRequired, Any


## User
class User(TypedDict):
    id: int
    username: str
    email: str
    points: int
    locale: str
    avatar: str
    type: str
    premium: int
    expiration: str


## Unrestrict
class UnrestrictCheck(TypedDict):
    host: str
    link: str
    filename: str
    filesize: int
    supported: int


class UnrestrictLink(TypedDict):
    id: str
    filename: str
    mimeType: str
    filesize: str
    link: str
    host: str
    chunks: int
    crc: int
    download: str
    streamable: int


class Alternative(TypedDict):  #
    id: str
    filename: str
    download: str
    type: str


class UnrestrictLinkMultiple(TypedDict):
    id: str
    filename: str
    mimeType: str
    filesize: str
    link: str
    host: str
    chunks: int
    crc: int
    download: str
    streamable: int
    type: str
    alternative: List[Alternative]


## Streaming
class Und1(TypedDict):  #
    stream: str
    lang: str
    lang_iso: str
    codec: str
    sampling: int
    channels: float
    colorspace: str
    width: int
    height: int


class Subtitle(TypedDict):  #
    stream: str
    lang: str
    lang_iso: str
    type: str


class VideoOrAudio(TypedDict):  #
    und1: Und1


class Details(TypedDict):  #
    video: VideoOrAudio
    audio: VideoOrAudio
    subtitles: List[Subtitle]


class StreamingMediaInfos(TypedDict):
    filename: str
    hoster: str
    link: str
    type: str
    season: str
    episode: str
    year: str
    duration: float
    bitrate: int
    size: int
    details: Details
    poster_path: str
    audio_image: str
    backdrop_path: str


## Downloads
class Downloads(TypedDict):
    id: str
    filename: str
    mimeType: str
    filesize: int
    link: str
    host: str
    chunks: int
    download: str
    generated: str
    type: NotRequired[str]


## Torrents
class Torrents(TypedDict):
    id: str
    filename: str
    hash: str
    bytes: int
    host: str
    split: int
    progress: int
    status: str
    added: str
    links: List[str]
    ended: str
    speed: NotRequired[int]
    seeders: NotRequired[int]


class File(TypedDict):  #
    id: int
    path: str
    bytes: int
    selected: int


class TorrentsInfo(TypedDict):
    id: str
    filename: str
    original_filename: str
    hash: str
    bytes: int
    original_bytes: int
    host: str
    split: int
    progress: int
    status: str
    added: str
    files: List[File]
    links: List[str]
    ended: NotRequired[str]
    speed: NotRequired[int]
    seeders: NotRequired[int]


class TorrentsActiveCount(TypedDict):
    nb: int
    limit: int


class TorrentsAvailableHosts(TypedDict):
    host: str
    max_file_size: int


class TorrentsAddTorrentOrMagnet(TypedDict):
    id: str
    uri: str


## Settings
class Settings(TypedDict):
    download_ports: List[Any]
    download_port: str
    locales: Any
    locale: str
    streaming_qualities: List[Any]
    streaming_quality: str
    mobile_streaming_quality: str
    streaming_languages: Any
    streaming_language_preference: str
    streaming_cast_audio: List[Any]
    streaming_cast_audio_preference: str
