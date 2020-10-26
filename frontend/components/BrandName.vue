<template>
<div class="container-fluid">
    <b-navbar variant="warning">
        <b-navbar-brand class="lead"><strong>Social Network - {{ form }}</strong></b-navbar-brand>
    </b-navbar>
</div>
  
</template>

<script>
export default {
    name: 'BrandName',
    props: {
        form: String
    }
    
}
</script>

<style>

</style>