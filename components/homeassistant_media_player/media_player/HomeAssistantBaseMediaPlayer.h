#pragma once

#include <algorithm>
#include <map>
#include <memory>
#include <string>
#include <vector>
#include "MediaPlayerSource.h"
#include "esphome/components/api/custom_api_device.h"
#include "esphome/components/media_player/media_player.h"

namespace esphome {
namespace homeassistant_media_player {

// enum MediaPlayerSupportedState {
//   MEDIA_CONTENT_ID,
//   MEDIA_CONTENT_TYPE,
//   MEDIA_SERIES_TITLE,
//   MEDIA_SEASON,
//   MEDIA_EPISODE,
//   MEDIA_CONTENT_RATING,
//   MEDIA_LIBRARY_TITLE,
//   MEDIA_SUMMARY,
//   MEDIA_TITLE,
//   MEDIA_ARTIST,
//   MEDIA_ALBUM_NAME,
//   MEDIA_ALBUM_ARTIST
// };

enum MediaPlayerSupportedFeature {
  PAUSE = 1,
  SEEK = 2,
  VOLUME_SET = 4,
  VOLUME_MUTE = 8,
  PREVIOUS_TRACK = 16,
  NEXT_TRACK = 32,
  TURN_ON = 128,
  TURN_OFF = 256,
  PLAY_MEDIA = 512,
  VOLUME_STEP = 1024,
  SELECT_SOURCE = 2048,
  STOP = 4096,
  CLEAR_PLAYLIST = 8192,
  PLAY = 16384,
  SHUFFLE_SET = 32768,
  SELECT_SOUND_MODE = 65536,
  BROWSE_MEDIA = 131072,
  REPEAT_SET = 262144,
  GROUPING = 524288,

  // bonus features
  TV_BACK = 9,
  TV_HOME = 10,
  MENU_HOME = 11,
  REMOTE_MODE = 12
};

static std::string supported_feature_string(
    MediaPlayerSupportedFeature feature) {
  switch (feature) {
    case PAUSE:
      return "Pause";
    case SEEK:
      return "Seek";
    case VOLUME_SET:
      return "Volume Set";
    case VOLUME_MUTE:
      return "Mute";
    case PREVIOUS_TRACK:
      return "Previous Track";
    case NEXT_TRACK:
      return "Next Track";
    case TURN_ON:
      return "Turn On";
    case TURN_OFF:
      return "Turn Off";
    case PLAY_MEDIA:
      return "Play Media";
    case VOLUME_STEP:
      return "Volume Step";
    case SELECT_SOURCE:
      return "Select Source";
    case STOP:
      return "Stop";
    case CLEAR_PLAYLIST:
      return "Clear Playlist";
    case PLAY:
      return "Play";
    case SHUFFLE_SET:
      return "Shuffle";
    case SELECT_SOUND_MODE:
      return "Select Sound Mode";
    case BROWSE_MEDIA:
      return "Browse Media";
    case REPEAT_SET:
      return "Repeat";
    case GROUPING:
      return "Grouping";
    case TV_BACK:
      return "Back";
    case TV_HOME:
      return "TV Home";
    case MENU_HOME:
      return "Menu";
    case REMOTE_MODE:
      return "Remote";
  }
  return "";
}

static std::map<MediaPlayerSupportedFeature, std::string>
    supported_feature_string_map = {
        {PAUSE, "PAUSE"},
        {SEEK, "SEEK"},
        {VOLUME_SET, "VOLUME_SET"},
        {VOLUME_MUTE, "VOLUME_MUTE"},
        {PREVIOUS_TRACK, "PREVIOUS_TRACK"},
        {NEXT_TRACK, "NEXT_TRACK"},
        {TURN_ON, "TURN_ON"},
        {TURN_OFF, "TURN_OFF"},
        {PLAY_MEDIA, "PLAY_MEDIA"},
        {VOLUME_STEP, "VOLUME_STEP"},
        {SELECT_SOURCE, "SELECT_SOURCE"},
        {STOP, "STOP"},
        {CLEAR_PLAYLIST, "CLEAR_PLAYLIST"},
        {PLAY, "PLAY"},
        {SHUFFLE_SET, "SHUFFLE_SET"},
        {SELECT_SOUND_MODE, "SELECT_SOUND_MODE"},
        {BROWSE_MEDIA, "BROWSE_MEDIA"},
        {REPEAT_SET, "REPEAT_SET"},
        {GROUPING, "GROUPING"},
};

enum RemotePlayerType { TVRemotePlayerType, SpeakerRemotePlayerType };

enum RemotePlayerState {
  NoRemotePlayerState,
  UnavailableRemotePlayerState,
  PowerOffRemotePlayerState,
  StoppedRemotePlayerState,
  PausedRemotePlayerState,
  PlayingRemotePlayerState
};

class HomeAssistantBaseMediaPlayer : public media_player::MediaPlayer,
                                     public Component {
 public:
  std::string mediaTitle = "";
  std::string mediaArtist = "";
  RemotePlayerMediaSource mediaSource = NoRemotePlayerMediaSource;
  RemotePlayerState playerState = NoRemotePlayerState;
  std::vector<std::shared_ptr<MediaPlayerSource>> sources;
  int index;
  virtual RemotePlayerType get_player_type() { return player_type_; }
  void setup() override;
  void playSource(MediaPlayerSource source);
  void playPause();
  void nextTrack();
  std::string mediaTitleString();
  std::string mediaSubtitleString();
  void clearMedia();
  std::string entity_id_;
  void set_entity_id(const std::string& entity_id) { entity_id_ = entity_id; }
  std::string get_entity_id() { return entity_id_; }
  bool is_muted() const override { return this->muted_; }
  bool is_shuffling() const { return this->shuffle_; }
  void toggle_shuffle();
  void toggle_mute();
  std::vector<std::shared_ptr<MediaPlayerSupportedFeature>> get_features() {
    return supported_features_;
  }
  std::vector<std::shared_ptr<MediaPlayerSupportedFeature>>
  get_option_menu_features() {
    std::vector<std::shared_ptr<MediaPlayerSupportedFeature>> out;
    std::copy_if(supported_features_.begin(), supported_features_.end(),
                 std::back_inserter(out),
                 [](std::shared_ptr<MediaPlayerSupportedFeature> i) {
                   switch (*(i.get())) {
                     case SHUFFLE_SET:
                     case VOLUME_MUTE:
                     case CLEAR_PLAYLIST:
                     case GROUPING:
                     case REPEAT_SET:
                     case TURN_ON:
                     case TURN_OFF:
                     case TV_BACK:
                     case TV_HOME:
                     case MENU_HOME:
                     case PAUSE:
                       //  case REMOTE_MODE:
                       return true;
                     default:
                       return false;
                   }
                 });
    return out;
  }

  bool supports(MediaPlayerSupportedFeature feature);

  virtual void increaseVolume();
  virtual void decreaseVolume();
  virtual void updateVolumeLevel();
  virtual void clearSource() {}
  virtual void media_artist_changed(std::string state);

  int mediaDuration = -1;
  int mediaPosition = -1;
  std::string playlist_title = "";
  std::vector<std::string> groupMembers;

 protected:
  bool muted_ = false;
  bool shuffle_ = false;
  float volume_step_ = 0.04;
  std::vector<std::shared_ptr<MediaPlayerSupportedFeature>>
      supported_features_ = {};

  void call_homeassistant_service(
      const std::string& service_name,
      const std::map<std::string, std::string>& data) {
    api::HomeassistantServiceResponse resp;
    resp.service = service_name;
    for (auto& it : data) {
      api::HomeassistantServiceMap kv;
      kv.key = it.first;
      kv.value = it.second;
      resp.data.push_back(kv);
    }
    api::global_api_server->send_homeassistant_service_call(resp);
  }

  virtual void subscribe_source() {}
  virtual void subscribe_sources() {}
  virtual void sources_changed(std::string state) {}
  virtual void group_members_changed(std::string state) {}
  virtual void subscribe_media_artist();

 private:
  RemotePlayerType player_type_;

  void selectSource(MediaPlayerSource source);
  void playMedia(MediaPlayerSource source);

  // subscriptions
  void subscribe_player_state();
  void subscribe_supported_features();
  void subscribe_media_title();
  void subscribe_muted();
  void subscribe_shuffle();
  void subscribe_volume();
  void subscribe_media_position();
  void subscribe_playlist();
  void subscribe_group_members();

  // changes
  void playerState_changed(std::string state);
  void player_supported_features_changed(std::string state);
  void media_title_changed(std::string state);
  void muted_changed(std::string state);
  void shuffle_changed(std::string state);
  void volume_changed(std::string state);
  void media_duration_changed(std::string state);
  void media_position_changed(std::string state);
  void playlist_changed(std::string state);
};
}  // namespace homeassistant_media_player
}  // namespace esphome
