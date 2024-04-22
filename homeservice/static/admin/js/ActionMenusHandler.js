// for action menu of any table
const actionMenus = document.querySelectorAll(".table_option-menu")
const actionOptions = document.querySelectorAll(".table_action_options")

// console.log(actionOptions);
actionMenus && actionMenus.forEach((actionMenu) => {
    actionMenu.addEventListener("click", () => {
        const arr = Object.values(actionMenus)
        const otherActionMenus = arr.filter(otherActionMenu => otherActionMenu !== actionMenu)
        otherActionMenus.forEach(menu => {
            menu.classList.remove("visible")
        })
        actionMenu.classList.toggle("visible")
    })
})

// for closing action menu when clicked outside
window.addEventListener("click", (e) => {
    if (!e.target.closest(".table_option-menu")) {
        actionMenus && actionMenus.forEach(menu => {
            menu.classList.remove("visible")
        })
    }
})

const customOption = document.querySelector(".table_action_options")
const showCustomOption = () => {
    customOption && (
        customOption.classList.add("visible")
    )
}

const hideCustomOption = () => {
    customOption && (
        customOption.classList.remove("visible")
    )
}