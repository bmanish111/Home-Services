var employeeId = document.getElementById('employeeID').value
const socket = new WebSocket(`ws://${window.location.host}/ws/employee/${employeeId}/`)
socket.onmessage = function (event) {
    const data = JSON.parse(event.data)
    console.log(data.message)
    notification_div = document.querySelector('.notification')
    if (data.type === 'notification.message') {
        /* notification_div.appendChild(document.createElement('div')).innerHTML = `
                                                                                                                                  <div class="alert alert-info" role="alert" id=notification_msg >${data.message}</div>
                                                                                                                                `
                notification_div
                setTimeout(() => {
                  notification_div.innerHTML = ''
                }, 5000)
            */
        // Generate a unique ID for each notification
        const notificationId = 'notification_' + new Date().getTime()

        // Create a new child div with the unique ID
        const newChild = document.createElement('div')
        newChild.id = notificationId
        // newChild.classList.add('alert', 'alert-info')
        // newChild.role = 'alert'
        // newChild.classList.add('alert', 'alert-info', 'alert-dismissible', 'fade', 'show')

        newChild.innerHTML = `
                              <div class="alert alert-info" role="alert">${data.message}</div>
                            `

        // Append the new child to the notification_div
        notification_div.appendChild(newChild)

        // Set a timeout to remove the specific child after 5 seconds
        setTimeout(() => {
            const elementToRemove = document.getElementById(notificationId)
            if (elementToRemove) {
                elementToRemove.remove()
            }
        }, 5000)
    }
}