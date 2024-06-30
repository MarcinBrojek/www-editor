document.addEventListener('DOMContentLoaded', function(){
    // all objects load
    // main
    const body = document.body
    const root = document.querySelector(':root')
    const style = getComputedStyle(root)
    // main windows
    const menu = document.getElementById('menu')
    const main = document.getElementById('main')
    const files = document.getElementById('files')
    const editor = document.getElementById('editor')
    const view = document.getElementById('view')
    const tabs = document.getElementById('tabs')
    const code = document.getElementById('code')
    const details = document.getElementById('details')
    // main windows contents - buttons
    const filesContent = document.getElementById('files-content')
    const detailsContent = document.getElementById('details-content')
    const tabContent = document.getElementById('tab-content')
    // windows from code
    const codeContent = document.getElementById('code-content')
    const codeInfo = document.getElementById('code-info')
    const addInfo = document.getElementById('file-dir-sect-add')
    const removeInfo = document.getElementById('file-dir-sect-remove')
    // main bar buttons part 1
    const fileButton = document.getElementById('menu-button1')
    const backButton = document.getElementById('menu-button-1a')
    const upButton = document.getElementById('menu-button-1b')
    const downButton = document.getElementById('menu-button-1c')
    const inButton = document.getElementById('menu-button-1d')
    // main bar buttons part 2
    const editButton = document.getElementById('menu-button2')
    const addButton = document.getElementById('menu-button-2a')
    const removeButton = document.getElementById('menu-button-2b')
    // other main buttons
    const rerunButton = document.getElementById('menu-button3')
    const codeButton = document.getElementById('menu-button4')
    const helpButton = document.getElementById('menu-button5')
    const projectButton = document.getElementById('menu-button6')
    const detailsButton = document.getElementById('menu-button7')
    const tabsButton = document.getElementById('menu-button8')
    const modeButton = document.getElementById('menu-button9')
    const profileButton = document.getElementById('menu-button10')
    // buttons from bottom bar
    const tabButton1 = document.getElementById('tab-button1')
    const tabButton2 = document.getElementById('tab-button2')
    const tabButton3 = document.getElementById('tab-button3')
    //const tabButton4 = document.getElementById('tab-button4')
    //buttons from code window
    const codeAddButton = document.getElementById('code-add-button')
    const codeRemoveButton = document.getElementById('code-remove-button')
    // contents from bottom window
    const tabContent1 = document.getElementById('tab-content1')
    const tabContent2 = document.getElementById('tab-content2')
    const tabContent3 = document.getElementById('tab-content3')
    //const tabContent4 = document.getElementById('tab-content4')
    // bars
    const leftBar = document.getElementById('left-bar')
    const rightBar = document.getElementById('right-bar')
    const bottomBar = document.getElementById('bottom-bar')
    // for edit - add
    const addedCategory = document.getElementById('added-category')
    const labelCategory = document.getElementById('label-category')
    const addedContent = document.getElementById('added-content')
    const labelContent = document.getElementById('label-content')
    const addedNumber = document.getElementById('added-number')
    const labelNumber = document.getElementById('label-number')
    const selectAddedType = document.getElementById('select-added-type');
    // const directoryOption = document.getElementById('directory-option')
    // const fileOption = document.getElementById('file-option')
    // const sectionOption = document.getElementById('section-option')
    // for edit - remove
    const selectRemovedButton = document.getElementById('select-removed-button')
    const selectRemovedType = document.getElementById('select-removed-type')
    const removedName = document.getElementById('removed-name')
    // for help
    const helpWindow = document.getElementById('help-window')
    // for profile
    const profileWindow = document.getElementById('profile-window')
    console.log(profileWindow)
    const loginInfo = document.getElementById('login-info')
    const loginWindow = document.getElementById('login-section')
    const registerWindow = document.getElementById('register-section')
    const loginButton = document.getElementById('login-button')
    const registerLink = document.getElementById('register-link')
    const registerButton = document.getElementById('register-button')
    const logoutButton = document.getElementById('logout')
    // area for code
    const addArea = CodeMirror(addedContent, {
        mode:  "text/x-csrc",
        autoRefresh: true
    })
    let codeArea = CodeMirror(codeContent, {
        mode:  "text/x-csrc",
        readOnly: true,
    })
    // sth helpful
    const calcJs = document.getElementById('calcJs')

    // user
    let user = null

    // color set - mode

    let darkMode = false // false => light, true => dark
    let properties = ['--bg-menu', '--bg-files', '--bg-code', '--bg-details', '--bg-tab-selector', '--bg-tab-content', '--bg-bar', '--text-main-color', '--text-code-color']
    let lightProperties = ['--bg-light-menu', '--bg-light-files', '--bg-light-code', '--bg-light-details', '--bg-light-tab-selector', '--bg-light-tab-content', '--bg-light-bar', '--text-light-main-color', '--text-light-code-color']
    let darkProperties = ['--bg-dark-menu', '--bg-dark-files', '--bg-dark-code', '--bg-dark-details', '--bg-dark-tab-selector', '--bg-dark-tab-content', '--bg-dark-bar', '--text-dark-main-color', '--text-dark-code-color']

    let bgColor = Array(9)
    properties.forEach((el, i) => {bgColor[i]=style.getPropertyValue(el); i++})
    properties.forEach((el, i) => {root.style.setProperty(el, bgColor[i]); i++})

    let bgLightColor = Array(9)
    lightProperties.forEach((el, i) => {bgLightColor[i]=style.getPropertyValue(el); i++})

    let bgDarkColor = Array(9)
    darkProperties.forEach((el, i) => {bgDarkColor[i]=style.getPropertyValue(el); i++})

    modeButton.addEventListener('click', clickMode, false)

    function clickMode() {
        if (darkMode === true) {
            darkMode = false
            properties.forEach((el, i) => {root.style.setProperty(el, bgLightColor[i]); i++})
        } else {
            darkMode = true
            properties.forEach((el, i) => {root.style.setProperty(el, bgDarkColor[i]); i++})
        }
        reloadColor()
    }

    // tabs buttons

    const tabButtons = [tabButton1, tabButton2, tabButton3] //,tabButton4]
    const tabContents = [tabContent1, tabContent2, tabContent3] //, tabContent4]
    let actualClicked = 0, tabNumber = 3 // 4

    for (let i = 0; i < tabNumber; i++) {
        tabButtons[i].addEventListener('click', () => clickBackground(i), false)
    }

    function clickBackground(number) {
        tabButtons[actualClicked].style.background = root.style.getPropertyValue('--bg-tab-selector')
        tabButtons[actualClicked].style.color = root.style.getPropertyValue('--text-main-color')
        tabContents[actualClicked].style.display = 'none'
        tabButtons[number].style.background = root.style.getPropertyValue('--bg-tab-content')
        tabButtons[number].style.color = root.style.getPropertyValue('--text-code-color')
        tabContents[number].style.display = 'block'
        actualClicked = number
    }

    clickBackground(0);

    function reloadColor() {
        for (let i = 0; i < tabNumber; i++) {
            tabButtons[i].style.background = root.style.getPropertyValue('--bg-tab-selector')
            tabButtons[i].style.color = root.style.getPropertyValue('--text-main-color')
        }
        tabButtons[actualClicked].style.background = root.style.getPropertyValue('--bg-tab-content')
        tabButtons[actualClicked].style.color = root.style.getPropertyValue('--text-code-color')
    }

    // show / hide - menu rights buttons: projects, details, tabs

    let lastPercent = [] // all changes while resize
    countLastPercent()

    projectButton.addEventListener('click', () => showHideWindow(1, files, editor, main), false)
    detailsButton.addEventListener('click', () => showHideWindow(2, details, code, view), false)
    tabsButton.addEventListener('click', () => showHideWindow(3, tabs, view, editor), false)

    function showHideWindow(number, win1, win2, allWin) {
        if (number === 3) {
            calcJs.style.height = 'calc(3vh + 3px)'
            if (win1.offsetHeight === calcJs.offsetHeight) {
                setNormalPadding(tabContent)
                win1.style.height = lastPercent[number] + '%'
                win2.style.height = 100 - lastPercent[number] + '%'
            } else {
                erasePadding(tabContent)
                lastPercent[number] = win1.offsetHeight / allWin.offsetHeight * 100
                win1.style.height = 'calc(3vh + 3px)'
                win2.style.height = 'calc(100% - 3vh - 3px)'
            }
        } else {
            if (win1.style.width === '3px') {
                if (win1 === files) {
                    setNormalPadding(filesContent)
                } else {
                    setNormalPadding(detailsContent)
                }
                win1.style.width = lastPercent[number] + '%'
                win2.style.width = 100 - lastPercent[number] + '%'
            } else {
                if (win1 === files) {
                    erasePadding(filesContent)
                } else {
                    erasePadding(detailsContent)
                }
                lastPercent[number] = win1.offsetWidth / allWin.offsetWidth * 100
                win1.style.width = '3px'
                win2.style.width = 'calc(100% - 3px)'
            }
        }
    }

    function countLastPercent() {
        if (files.offsetWidth !== 3) {
            lastPercent[0] = files.offsetWidth / main.offsetWidth * 100
        }
        if (details.offsetWidth !== 3) {
            lastPercent[1] = details.offsetWidth / view.offsetWidth * 100
        }
        calcJs.style.height = 'calc(3vh + 3px)'
        if (tabs.offsetHeight !== calcJs.offsetHeight) {
            lastPercent[2] = tabs.offsetHeight / editor.offsetHeight * 100
        }
    }

    // bars - left, right, bottom to resize

    leftBar.addEventListener('mousedown', leftBarResize, false)
    rightBar.addEventListener('mousedown', rightBarResize, false)
    bottomBar.addEventListener('mousedown', bottomBarResize, false)

    leftBar.style.cursor = 'col-resize'
    rightBar.style.cursor = 'col-resize'
    bottomBar.style.cursor = 'row-resize'

    let posX = null, posY = null
    let partPx, allPx
    let bar = null

    function countPartPercent(deltaPx, x) {
        return Math.max(25*x, Math.min(allPx - 50*x, partPx + deltaPx)) / allPx * 100
    }

    function leftBarResize(e) {
        e.preventDefault()
        bar = [files, editor]
        partPx = bar[0].offsetWidth
        allPx = partPx + bar[1].offsetWidth
        posX = e.clientX
        startStopResize("vertical")
    }

    function rightBarResize(e) {
        e.preventDefault()
        bar = [code, details]
        partPx = bar[0].offsetWidth
        allPx = partPx + bar[1].offsetWidth
        posX = e.clientX
        startStopResize("vertical")
    }

    function bottomBarResize(e) {
        e.preventDefault()
        bar = [view, tabs]
        partPx = bar[0].offsetHeight
        allPx = partPx + bar[1].offsetHeight
        posY = e.clientY
        startStopResize("horizontal")
    }

    function startStopResize(direction) {
        if (direction === "vertical") {
            window.addEventListener('mousemove', startVerticalResize, false)
            window.addEventListener('mouseup', stopVerticalResize, false)
        }
        if (direction === "horizontal") {
            window.addEventListener('mousemove', startHorizontalResize, false)
            window.addEventListener('mouseup', stopHorizontalResize, false)
        }
    }

    function startVerticalResize(e) {
        let nextPercentWidth = countPartPercent(e.clientX - posX, 3)
        bar[0].style.width =  nextPercentWidth + '%'
        bar[1].style.width =  100 - nextPercentWidth + '%'
        if (bar[0] === files) {
            setNormalPadding(filesContent)
        } else {
            setNormalPadding(detailsContent)
        }
    }

    function stopVerticalResize() {
        countLastPercent()
        window.removeEventListener('mousemove', startVerticalResize, false)
        window.removeEventListener('mouseup', stopVerticalResize, false)
    }

    function startHorizontalResize(e) {
        let nextPercentHeight = countPartPercent(e.clientY - posY, 1)
        bar[0].style.height =  nextPercentHeight + '%'
        bar[1].style.height =  100 - nextPercentHeight + '%'
        setNormalPadding(tabContent)
    }

    function stopHorizontalResize() {
        countLastPercent()
        window.removeEventListener('mousemove', startHorizontalResize, false)
        window.removeEventListener('mouseup', stopHorizontalResize, false)
    }

    // padding set

    function setNormalPadding(object) {
        object.style.setProperty('padding', '5px')
    }

    function erasePadding(object) {
        object.style.setProperty('padding', '0px')
    }

    // js for resizing global window
    // automatic change of windows sizes

    window.addEventListener('resize', actualizeWindows)

    function actualizeWindows() {
        if (window.innerHeight < 720 || window.innerWidth < 1024) {
            tabs.style.removeProperty('width')
            code.style.removeProperty('width')
            details.style.removeProperty('width')
            files.style.removeProperty('width')
            filesContent.style.removeProperty('width')
            editor.style.removeProperty('width')
            detailsContent.style.removeProperty('width')
            body.style.removeProperty('height')
            menu.style.removeProperty('height')
            main.style.removeProperty('height')
            view.style.removeProperty('height')
            tabs.style.removeProperty('height')
            tabContent.style.removeProperty('height')
            tabContent.style.setProperty('padding', '5px')
            filesContent.style.setProperty('padding', '5px')
            detailsContent.style.setProperty('padding', '5px')
        }
    }

    // all helper buttons in main bar, code window buttons - edit

    let fileButtons = [backButton, downButton, upButton, inButton]
    let editButtons = [addButton, removeButton]
    let helperButtons = [backButton, downButton, upButton, inButton, addButton, removeButton]
    let visibleFile = 0
    let visibleEdit = 0
    let visibleHelp = 0
    let visibleContentCode = 0
    let visibleProfile = 0

    let codeWindows = [codeContent, codeInfo]
    let visibleCodeInfo = 0
    let visibleAddInfo = 0
    let visibleRemoveInfo = 0

    let cantUseArrowsForFiles = false

    function showButtons(buttons) {
        buttons.forEach((button) => button.style.removeProperty('display'))
    }
    function hideHelperButtons() {
        cantUseArrowsForFiles = false
        helperButtons.forEach((button) => button.style.setProperty('display', 'none'))
        visibleFile = 0
        visibleEdit = 0
    }

    function showCodeWindow(wind) {
        cantUseArrowsForFiles = true
        wind.style.removeProperty('display')
    }
    function hideCodeWindows() {
        cantUseArrowsForFiles = false
        codeWindows.forEach((wind) => wind.style.setProperty('display', 'none'))
        visibleCodeInfo = 0
        visibleAddInfo = 0
        visibleRemoveInfo = 0
    }

    function safeHideAllVisible() {
        hideHelperButtons()
        hideCodeWindows()
        visibleProfile = 0
        visibleHelp = 0
        visibleContentCode = 0
        hideHelpWindow()
        hideProfileWindow()
    }
    safeHideAllVisible()

    // buttons for file section
    // back, up, down, in

    fileButton.addEventListener('click', () => showFileButtons(), false)

    function showFileButtons() {
        if (visibleFile === 0) {
            safeHideAllVisible()
            showButtons(fileButtons)
            visibleFile = 1;
        }
        else {
            safeHideAllVisible()
        }
    }

    // file section operations from file, focus section operations

    let actualFile = null
    let listDives = []
    let listFiles = []
    let size = 0
    let actualPosition = 0

    let rerunType = "alt-ergo"
    let rteOption = false
    let propOption = false
    let propContent = ""
    let listDivSections = []
    let listVisibleSection = []

    function clearFocusDives() {
        for (let i = 0; i < listDivSections.length; i++) {
            listDivSections[i].remove()
        }
        listDivSections = []
        listVisibleSection = []
    }

    function showSectionContent(pos) {
        if (listVisibleSection[pos] === 1) {
            listDivSections[pos * 2 + 1].style.setProperty('display', 'none')
            listVisibleSection[pos] = 0
        } else {
            listDivSections[pos * 2 + 1].style.removeProperty('display')
            listVisibleSection[pos] = 1
        }
    }

    function addFocusElement(section) {
        let tmpNameElement = document.createElement("div")
        tmpNameElement.style.setProperty('width', '100%')
        tmpNameElement.style.setProperty('text-align', 'center')
        tmpNameElement.style.setProperty('margin-top', '10px')
        tmpNameElement.style.setProperty('border-top', 'double')
        tmpNameElement.style.setProperty('border-bottom', 'double')
        tmpNameElement.style.setProperty('cursor', 'pointer')
        tmpNameElement.textContent = section.name
        let tmpContentElement = document.createElement("div")
        tmpContentElement.style.setProperty('width', '100%')
        tmpContentElement.style.setProperty('white-space', 'pre')
        tmpContentElement.textContent = section.content
        tmpContentElement.style.setProperty('display', 'none')

        let pos = listVisibleSection.length
        listDivSections.push(tmpNameElement)
        listDivSections.push(tmpContentElement)
        detailsContent.appendChild(tmpNameElement)
        detailsContent.appendChild(tmpContentElement)
        listVisibleSection.push(0)

        tmpNameElement.addEventListener('click', () => showSectionContent(pos), false)
    }

    function addFilesElement(name) {
        let tmpFilesElement = document.createElement("div")
        tmpFilesElement.style.setProperty('width', '100%')
        tmpFilesElement.style.setProperty('padding-top', '10px')
        tmpFilesElement.style.setProperty('text-align', 'center')
        if (listFiles[size].type === 'Directory') {
            tmpFilesElement.style.setProperty('font-weight', 'bold')
            tmpFilesElement.textContent += '📁  '
        }
        if (listFiles[size].type === 'File') {
            tmpFilesElement.textContent += '📃  '
        }
        if (listFiles[size].type === 'FileSection') {
            tmpFilesElement.textContent += '📎 '
        }
        tmpFilesElement.textContent += name

        listDives.push(tmpFilesElement)
        size += 1
        filesContent.appendChild(tmpFilesElement)
    }

    function sortFiles() {
        let files = []
        let catalogs = []
        let sections = []
        for (let i = 0; i < listFiles.length; i++) {
            if (listFiles[i].type === 'File') {
                files.push(listFiles[i])
            }
            if (listFiles[i].type === 'Directory') {
                catalogs.push(listFiles[i])
            }
            if (listFiles[i].type === 'FileSection') {
                sections.push(listFiles[i])
            }
        }
        listFiles = catalogs.concat(files)
        listFiles = listFiles.concat(sections)
    }

    function selectOther(mod) {
        if (size === 0) {
            return
        }
        listDives[actualPosition].style.removeProperty('text-decoration')
        actualPosition += mod
        if (actualPosition < 0) {
            actualPosition += size
        }
        actualPosition %= size
        listDives[actualPosition].style.setProperty('text-decoration', 'underline')
    }

    function clearFileDives() {
        for (let i = 0; i < listDives.length; i++) {
            listDives[i].remove()
        }
        listDives = []
        listFiles = []
        size = 0
        actualPosition = 0
    }

    function fillFilesLists() {
        clearFileDives()
        clearFocusDives()
        tabContent3.textContent=""
        let parentType = actualFile !== null ? actualFile.type : "Directory"
        let parentId = actualFile !== null ? actualFile.id : ""
        return new Promise(function(resolve, reject) {
            $.ajax({
                type: 'GET',
                url: 'get/ajax/files_list',
                data: {
                    'parent_type': parentType,
                    'parent_id': parentId
                },
                success: function(response) {
                    listFiles = response['list']
                    sortFiles()

                    for (let i = 0; i < listFiles.length; i++) {
                        addFilesElement(listFiles[i].name)
                    }
                    selectOther(0)

                    if (parentType === 'File') {
                        for (let i = 0; i < listFiles.length; i++) {
                            addFocusElement(listFiles[i])
                        }
                        tabContent3.textContent = actualFile.result
                    }

                    resolve(listFiles)
                },
                error: function(err) {
                    reject(err)
                }
            })
        })
    }

    function getFileList() {
        fillFilesLists().then(function(list) {
            console.log(list)
        }).catch(function(err) {
            console.log(err)
        })
    }

    getFileList()

    backButton.addEventListener('click', () => backAction(), false)
    function backAction() {
        console.log(actualFile)
        if (actualFile !== null && actualFile !== "") {
            if (actualFile.type === 'Directory' || actualFile.type === 'File') {
                actualFile = actualFile['parent_directory']
            }
            if (actualFile.type === 'FileSection') {
                if (actualFile['parent_file']) {
                    actualFile = actualFile['parent_file']
                }
                else {
                    actualFile = actualFile['parent_section']
                }
            }
        }
        getFileList()
    }

    downButton.addEventListener('click', () => downAction(), false)
    function downAction() {
        selectOther(1)
    }

    upButton.addEventListener('click', () => upAction(), false)
    function upAction() {
        selectOther(-1)
    }

    inButton.addEventListener('click', () => inAction(), false)
    function inAction() {
        if (size === 0) {
            return
        }
        actualFile = listFiles[actualPosition]
        getFileList()
    }

    // buttons add, remove from edit

    editButton.addEventListener('click', () => showEditButtons(), false)

    function showEditButtons() {
        if (visibleEdit === 0) {
            safeHideAllVisible()
            showButtons(editButtons)
            visibleEdit = 1
        }
        else {
            safeHideAllVisible()
        }
    }

    // operation add, remove from edit

    addButton.addEventListener('click', () => showAddWindow(), false)

    function showAddWindow() {
        if (visibleAddInfo === 0) {
            hideCodeWindows()
            showCodeWindow(codeInfo)
            removeInfo.style.setProperty('display', 'none')
            addInfo.style.removeProperty('display')
            visibleAddInfo = 1
        }
        else {
            hideCodeWindows()
            cantUseArrowsForFiles = false
        }
    }

    showDirectoryOption()

    function showDirectoryOption() {
        labelCategory.style.setProperty('display', 'none')
        addedCategory.style.setProperty('display', 'none')
        labelContent.style.setProperty('display', 'none')
        addedContent.style.setProperty('display', 'none')
        labelNumber.style.setProperty('display', 'none')
        addedNumber.style.setProperty('display', 'none')
    }
    function showFileOption() {
        labelCategory.style.setProperty('display', 'none')
        addedCategory.style.setProperty('display', 'none')
        labelContent.style.removeProperty('display')
        addedContent.style.removeProperty('display')
        labelNumber.style.setProperty('display', 'none')
        addedNumber.style.setProperty('display', 'none')
    }
    function showSectionOption() {
        labelCategory.style.removeProperty('display')
        addedCategory.style.removeProperty('display')
        labelContent.style.setProperty('display', 'none')
        addedContent.style.setProperty('display', 'none')
        labelNumber.style.removeProperty('display')
        addedNumber.style.removeProperty('display')
        console.log("abcd")
    }

    selectAddedType.addEventListener('change', function() {
        const selectedValue = selectAddedType.value
        if (selectedValue === 'Directory') {
            showDirectoryOption()
        }
        if (selectedValue === 'File') {
            showFileOption()
        }
        if (selectedValue === 'FileSection') {
            showSectionOption()
        }
    })

    codeAddButton.addEventListener('click', () => realizeAddRequest(), false)
    function addRequest() {
        let parentType = actualFile !== null ? actualFile.type : "Directory"
        let parentId = actualFile !== null ? actualFile.id : ""
        let line_number = $("#added-number").val()
        line_number = line_number !== '' ? line_number : 0
        let login = user !== null ? user.login : ""
        let password = user !== null ? user.password : ""

        return new Promise(function(resolve, reject) {
            $.ajax({
                type: 'GET',
                url: 'get/ajax/add',
                data: {
                    'login': login,
                    'password': password,
                    'type_name': $("#select-added-type :selected").val(),
                    'name': $("#added-name").val(),
                    'description': $("#added-description").val(),
                    'category': $("#added-category").val(),
                    'content': addArea.getValue(),
                    'line-number': line_number,
                    'parent_type': parentType,
                    'parent_id': parentId,
                },
                success: function(response) {
                    let info = response['info']
                    console.log(info)
                    resolve(info)
                },
                error: function(err) {
                    reject(err)
                }
            })
        })
    }
    function realizeAddRequest() {
        console.log('started action add')
        addRequest().then(function(err) {
            getFileList()
            console.log('done action add')
        }).catch(function(err) {
            console.log(err)
        })
    }

    removeButton.addEventListener('click', () => showRemoveWindow(), false)

    function showRemoveWindow() {
        if (visibleRemoveInfo === 0) {
            hideCodeWindows()
            showCodeWindow(codeInfo)
            addInfo.style.setProperty('display', 'none')
            removeInfo.style.removeProperty('display')
            visibleRemoveInfo = 1
        }
        else {
            hideCodeWindows()
            cantUseArrowsForFiles = false
        }
    }

    selectRemovedButton.addEventListener('click', () => fillRemoveFields(), false)
    function fillRemoveFields() {
        selectRemovedType.value = listFiles[actualPosition].type
        removedName.value = listFiles[actualPosition].name
    }

    codeRemoveButton.addEventListener('click', () => realizeRemoveRequest(), false)
    function removeRequest() {
        let parentType = actualFile !== null ? actualFile.type : "Directory"
        let parentId = actualFile !== null ? actualFile.id : ""
        let login = user !== null ? user.login : ""
        let password = user !== null ? user.password : ""

        return new Promise(function(resolve, reject) {
            $.ajax({
                type: 'GET',
                url: 'get/ajax/remove',
                data: {
                    'login': login,
                    'password': password,
                    'type_name': $("#select-removed-type :selected").val(),
                    'name': $("#removed-name").val(),
                    'parent_type': parentType,
                    'parent_id': parentId,
                },
                success: function(response) {
                    let info = response['info']
                    resolve(info)
                },
                error: function(err) {
                    reject(err)
                }
            })
        })
    }
    function realizeRemoveRequest() {
        console.log('started action remove')
        removeRequest().then(function(info){
            getFileList()
            console.log(info)
            console.log('done action remove')
        }).catch(function(err) {
            console.log(err)
        })
    }

    // help button

    helpButton.addEventListener('click', () => showHelpWindow(), false)

    function hideHelpWindow() {
        helpWindow.style.setProperty('display', 'none')
    }

    function showHelpWindow() {
        if (visibleHelp === 0) {
            safeHideAllVisible()
            helpWindow.style.removeProperty('display')
            visibleHelp = 1
        }
        else {
            safeHideAllVisible()
        }
    }

    // some shortcuts possible like arrows :

    window.addEventListener('keydown', e => {
        if (e.code === 'Escape') {
            safeHideAllVisible()
        }
        if (cantUseArrowsForFiles === true) {
            return
        }
        if (e.code === 'KeyH') {
            showHelpWindow()
            return
        }
        if (e.code === 'KeyF') {
            showFileButtons()
            return
        }
        if (e.code === 'KeyE') {
            showEditButtons()
            return
        }
        if (e.code === 'KeyA') {
            showEditButtons()
            showAddWindow()
            return
        }
        if (e.code === 'KeyR') {
            showEditButtons()
            showRemoveWindow()
            return
        }
        if (e.code === 'KeyT') {
            clickBackground((actualClicked + 1) % 3) // 4
            return
        }
        if (e.code === 'KeyC') {
            showContentCode()
            return
        }
        if (e.code === 'KeyM') {
            clickMode()
            return
        }
        if (e.code === 'KeyP') {
            showProfile()
            return
        }
        if (e.key === "ArrowLeft") {
            backAction()
            safeHideAllVisible()
            return
        }
        if (e.key === "ArrowUp") {
            upAction()
            safeHideAllVisible()
            return
        }
        if (e.key === "ArrowRight") {
            inAction()
            safeHideAllVisible()
            return
        }
        if (e.key === "ArrowDown") {
            downAction()
            safeHideAllVisible()
        }
    }, false)

    // code button - show code of file / section

    codeButton.addEventListener('click', () => showContentCode(), false)

    function hideContentCode() {
        codeContent.style.setProperty('display', 'none')
    }

    function showContentCode() {
        if (actualFile === null || actualFile === "" || actualFile.type === 'Directory') {
            return
        }

        if (visibleContentCode === 0) {
            safeHideAllVisible()
            let lineIndexLen = actualFile['end_line_number'].toString().length;
            console.log(lineIndexLen)
            let content = ""
            content = " ".repeat(lineIndexLen - 1) + "0| ";
            let i = 0, pos = 0, b = false
            for (let c of actualFile.content) {
                content += c

                if (c === '\n') {
                    i += 1
                    content += (" ".repeat(lineIndexLen - i.toString().length) + i.toString() + "| ")
                }
            }
            codeArea.setValue(content)
            codeContent.style.removeProperty('display')
            codeArea.refresh()
            visibleContentCode = 1
        }
        else {
            safeHideAllVisible()
        }
    }

    // login, logout, register - profile window


    function hideProfileWindow() {
        profileWindow.style.setProperty('display', 'none')
    }
    function hideProfileSections() {
        loginInfo.style.setProperty('display', 'none')
        loginWindow.style.setProperty('display', 'none')
        registerWindow.style.setProperty('display', 'none')
        logoutButton.style.setProperty('display', 'none')
    }

    profileButton.addEventListener('click', () => showProfile(), false)

    function showProfile() {
        if (visibleProfile === 0) {
            safeHideAllVisible()
            showCodeWindow(profileWindow)
            hideProfileSections()
            if (user !== null) {
                loginInfo.textContent = "Logged in as: " + user.login.toString()
                loginInfo.style.removeProperty('display')
                logoutButton.style.removeProperty('display')
                cantUseArrowsForFiles = false
            }
            else {
                loginWindow.style.removeProperty('display')
            }
            visibleProfile = 1
        }
        else {
            safeHideAllVisible()
            cantUseArrowsForFiles = false
        }
    }

    loginButton.addEventListener('click', () => loginRequest(), false)

    function loginRequest() {
        let login = $("#login-login").val()
        let password = $("#login-password").val()

        $.ajax({
            type: 'GET',
            url: 'get/ajax/log_in',
            data: {
                'login': login,
                'password': password,
            },
            success: function(response) {
                user = response['user']
                if (user === "") {
                    user = null
                    loginInfo.textContent = "Invalid provided login or password."
                }
                else {
                    loginInfo.textContent = "Logged in as: " + user.login.toString()
                }
                $("#login-login").value = ""
                $("#login-password").value = ""
                loginInfo.style.removeProperty('display')
            }
        })
    }

    registerLink.addEventListener('click', () => showRegisterWindow(), false)

    function showRegisterWindow() {
        hideProfileSections()
        registerWindow.style.removeProperty('display')
    }

    registerButton.addEventListener('click', () => registerRequest(), false)

    function registerRequest() {
        let name = $("#register-name").val()
        let login = $("#register-login").val()
        let password = $("#register-password").val()
        let repeated_password = $("#register-rep-password").val()
        console.log(login)
        $.ajax({
            type: 'GET',
            url: 'get/ajax/register',
            data: {
                'name': name,
                'login': login,
                'password': password,
                'repeated_password': repeated_password
            },
            success: function(response) {
                user = response['user']
                let err = response['err']
                if (user === "") {
                    user = null
                    loginInfo.textContent = err
                }
                else {
                    loginInfo.textContent = "Logged in as: " + user.login.toString()
                }
                loginInfo.style.removeProperty('display')
            }
        })
    }

    logoutButton.addEventListener('click', () => logout(), false)

    function logout() {
        user = null
        hideProfileSections()
        cantUseArrowsForFiles = true
        loginWindow.style.removeProperty('display')
        loginInfo.textContent = "Logged out."
        loginInfo.style.removeProperty('display')
    }

    // provers tab section

    const altButton = document.getElementById('Alt')
    const z3Button = document.getElementById('Z3')
    const cvc4Button = document.getElementById('CVC4')
    const proverComment = document.getElementById('prover-comment')

    function changeRerunType(name) {
        rerunType = name
        proverComment.textContent = "Chosen prover " + name + "."
    }
    changeRerunType("alt-ergo")

    altButton.addEventListener('click', () => changeRerunType("alt-ergo"), false)
    z3Button.addEventListener('click', () => changeRerunType("Z3"), false)
    cvc4Button.addEventListener('click', () => changeRerunType("CVC4"), false)

    // vcx tab section

    const rteButton = document.getElementById('rte')
    const propButton = document.getElementById('prop')
    const vcsComment = document.getElementById('vcs-comment')

    function changeVcsComment() {
        vcsComment.textContent = "Chosen vcs: \""
        if (propOption === true) {
            vcsComment.textContent += "-wp-prop=\""
            vcsComment.textContent += propContent
            vcsComment.textContent += "\" "
        }
        if (rteOption === true) {
            vcsComment.textContent += "-wp-rte "
        }
        vcsComment.textContent += "\""
    }
    changeVcsComment()

    rteButton.addEventListener('click', () => {
        rteOption=!rteOption; changeVcsComment()}, false)
    propButton.addEventListener('click', () => {
        propOption=!propOption; propContent=$("#prop-content").val(); changeVcsComment()}, false)

    // rerun button

    rerunButton.addEventListener('click', () => rerunRealize(), false)

    function rerun() {
        if (actualFile === "" || actualFile === null) {
            return
        }
        if (actualFile.type !== 'File') {
            return
        }
        let login = $("#login-login").val()
        let password = $("#login-password").val()
        let rte = rteOption === true ? "is rte" : ""

        return new Promise(function(resolve, reject) {
            $.ajax({
                type: 'GET',
                url: 'get/ajax/rerun',
                data: {
                    'login': login,
                    'password': password,
                    'file_id': actualFile.id,
                    'prover': rerunType,
                    'rte': rte,
                    'prop_content': propContent
                },
                success: function(response) {
                    resolve(response['ok'])
                },
                error: function(error) {
                    reject(error)
                }
            })
        })
    }

    function rerunRealize() {
        console.log('started action rerun')
        rerun().then(function(ok){
            if (ok) {
                getFileList()
                modifyResult()
            }
            console.log('done action rerun') // maybe done - modify maybe not ended
        }).catch(function(err) {
            console.log(err)
        })
    }

    // for rerun to modify result, only available in rerun!

    function modifyResult() {
        let login = $("#login-login").val()
        let password = $("#login-password").val()
        $.ajax({
            type: 'GET',
            url: 'get/ajax/rerun/result',
            data: {
                'login': login,
                'password': password,
                'file_id': actualFile.id,
            },
            success: function(response) {
                tabContent3.textContent = actualFile.result = response['result']
            }
        })
    }
})