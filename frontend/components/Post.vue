<template>
  <div class="media border p-1">
    <div class="media-body post-color p-1">
      <h5 class="lead mt-0">
        <strong> Title goes here! Username link or whatever.</strong>
      </h5>
      <p class="lead">
        Content can go here. Photos etc. Lorem, ipsum dolor sit amet consectetur
        adipisicing elit. Ex voluptatum enim fuga voluptas natus suscipit
        dolores consectetur in iure eveniet eos, sequi ducimus cumque, eius
        nostrum molestiae excepturi quibusdam quis.
      </p>

      <hr />

      <div class="ml-5">
        <div class="media">
          <div class="media-body" :class="{ 'post-font' : true}">
            <h5 class="mt-0">
              <strong
                >And look at this, we can make nested comments User can answer
                here for an instance!</strong
              >
            </h5>
            <p class="">
              Content can go here. Photos etc. Lorem, ipsum dolor sit amet
              consectetur adipisicing elit. Ex voluptatum enim fuga voluptas
              natus suscipit dolores consectetur in iure eveniet eos, sequi
              ducimus cumque, eius nostrum molestiae excepturi quibusdam quis.
            </p>

            <hr>

            <div class="ml-5">
              <div class="media">
                <div class="media-body" :class="{ 'post-font' : true}">
                  <h5 class=" mt-0">
                    <strong
                      >And look at this, we can make EVEN MORE nested
                      comments!!!!!!</strong
                    >
                  </h5>
                  <p class="">
                    Content can go here. Photos etc. Lorem, ipsum dolor sit amet
                    consectetur adipisicing elit. Ex voluptatum enim fuga
                    voluptas natus suscipit dolores consectetur in iure eveniet
                    eos, sequi ducimus cumque, eius nostrum molestiae excepturi
                    quibusdam quis.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Post hierarchy
      <div class="ml-5" v-for="comment in post.comments" :key="comment.Id">
        <Post post=""/>
      </div>
      -->
      
    </div>
  </div>
</template>

<script>
export default {
  name: "Post",
  props: {
    post: Object,
  },
};
</script>

<style>
</style>