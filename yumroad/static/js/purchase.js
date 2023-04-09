function purchase(stripe, checkout_session_id) {
    stripe.redirectToCheckout({
    sessionId: checkout_session_id
    }).then(function (result) {
    alert(result.error.message)
    });
}
