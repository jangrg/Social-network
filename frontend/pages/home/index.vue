<template>
  <div class="d-flex flex-column bg-pattern">
    <TopBar />
    <SideBar />
    

    <div class="container row white-container rounded p-2 mx-auto">
      <div>
        <h3>New posts</h3>
        <Post /> <!--TODO add post component, lorem just for demonstative purposes -->
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget
          hendrerit ligula. Donec tempor pellentesque lorem. Suspendisse ornare
          diam sit amet justo ullamcorper ornare. Maecenas nec ante accumsan,
          venenatis neque eget, ultrices lacus. Aliquam sem nunc, viverra nec
          lacus sed, gravida dapibus leo. Nam suscipit accumsan pharetra. Cras
          ante dui, ullamcorper non fringilla quis, eleifend nec nisi. Aenean ac
          velit nunc. Pellentesque sed arcu nec erat semper faucibus euismod non
          velit. Donec at ligula sollicitudin, vehicula eros eget, hendrerit
          arcu. Aliquam vestibulum luctus odio, eu mattis felis fringilla sed.
          Duis id elit tincidunt elit aliquet accumsan id non nulla. In rutrum
          ut tortor in vestibulum. Quisque euismod dui nec orci lacinia, id
          congue turpis malesuada. Quisque cursus ultrices elit at ultrices.
          Pellentesque porta orci ipsum, ac feugiat massa semper eu. Vivamus
          lobortis auctor ante vel euismod. Vestibulum arcu sapien, suscipit ac
          ultrices eget, facilisis sed arcu. In sit amet diam ex. Curabitur sit
          amet eleifend ex. Donec lorem quam, hendrerit sed enim id, gravida
          tristique nisl. Morbi a nunc sagittis, pharetra neque et, luctus nisi.
          Quisque in congue enim. Sed felis lorem, facilisis in tincidunt sit
          amet, rutrum sit amet mi. Vivamus nec ipsum at massa tincidunt commodo
          sed vel sem. Ut volutpat commodo tellus nec efficitur. Maecenas eget
          rhoncus ante. Ut sollicitudin ante id leo faucibus vestibulum. Proin
          auctor turpis dui, ut dictum quam lobortis euismod. Mauris nec
          sagittis mi. Donec sed tortor bibendum, sagittis nunc id, euismod
          libero. Etiam porta augue id ipsum varius tempus. Mauris luctus
          viverra magna. Vivamus egestas ante sit amet congue hendrerit. Donec
          vel vulputate lacus. Nullam imperdiet quis augue nec pulvinar. Nunc
          nec massa libero. Proin at aliquet leo, sed laoreet lacus. Phasellus
          feugiat odio nec consectetur ornare. Donec quis felis eget ex faucibus
          aliquam vel eget nulla. Mauris venenatis at nisl rutrum fringilla. Sed
          tortor sem, consequat eget quam sit amet, consectetur efficitur
          tellus. Cras elementum viverra pulvinar. Nullam feugiat mi ac diam
          mollis, vitae fringilla sem cursus. Proin eget tempor eros, sed
          maximus libero. Proin suscipit molestie lacus, in posuere nisl
          molestie eget. Proin congue cursus sapien, sed sagittis leo convallis
          vel. Cras in finibus purus. Duis eros nibh, varius vitae eleifend a,
          vestibulum in diam. Aliquam finibus ante nec velit aliquet,
          sollicitudin convallis neque ultrices. Phasellus pellentesque tempus
          diam, nec ullamcorper ante fermentum nec.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ButtonPlugin } from "bootstrap-vue";

import TopBar from "../../components/TopBar";

import SideBar from "../../components/SideBar";

export default {
  name: "Home",
  components: { TopBar, SideBar },
  head() {
    return {
      title: "Home",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no",
        },
      ],
    };
  },
  computed: {
    user() {
      return this.$store.state.User.user;
    },
  },
};
</script>

<style scoped>
</style>
