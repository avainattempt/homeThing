#pragma once

#include <memory>
#include <string>
#include <vector>
#include "HomeAssistantBaseMediaPlayer.h"

namespace esphome {
namespace homeassistant_media_player {

class HomeAssistantRokuMediaPlayer : public HomeAssistantBaseMediaPlayer {
 public:
  HomeAssistantBaseMediaPlayer* speaker;

  void setup() override;

  void player_source_changed(std::string state);

  void tvRemoteCommand(std::string command);
  void increaseVolume();
  void decreaseVolume();
  media_player::MediaPlayerTraits get_traits();
  void control(const media_player::MediaPlayerCall& call);
  RemotePlayerType get_player_type() { return TVRemotePlayerType; }
  void set_soundbar(HomeAssistantBaseMediaPlayer* new_sound_bar) {
    speaker = new_sound_bar;
  }

 private:
  void sources_changed(std::string state) override;
  void subscribe_sources() override;
  void group_members_changed(std::string state) {}
};
}  // namespace homeassistant_media_player
}  // namespace esphome
