export default {
  getUser() {
    return new Promise(function(resolve, reject){
      resolve({
        isAuthenticated: window.user_is_authenticated || false,
      })
    });
  }
}