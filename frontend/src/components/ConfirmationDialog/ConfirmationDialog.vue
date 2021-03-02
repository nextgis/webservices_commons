<template>
  <v-dialog class="confirmation-dialog" v-bind="$attrs" v-on="$listeners" :max-width="$attrs.maxWidth || defaultWidth">
    <v-card class="pa-4">
      <slot></slot>
      <div class="text-right pt-4">
        <slot name="buttons">
          <v-btn small flat color="primary" @click="$emit('cancel')">{{ btnFalseText }}</v-btn>
          <v-btn class="ml-1" small color="primary" @click="$emit('confirm')">{{ btnTrueText }}</v-btn>
        </slot>  
      </div>  
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    name: 'ConfirmationDialog',
    props: {
      btnTrueText: {
        type: String,
        default: 'Ok'
      },
      btnFalseText: {
        type: String,
        default: 'Cancel'
      }
    },
    data() {
      return {
        defaultWidth: 400
      }
    },
  }
</script>

<style lang="scss" scoped>

</style>