// Компоненты пользовательского интерфейса

class Button {
    constructor(text, onClick) {
        this.text = text;
        this.onClick = onClick;
    }
    
    render() {
        return `<button class="btn" onclick="${this.onClick}">${this.text}</button>`;
    }
}

class Modal {
    constructor(title, content) {
        this.title = title;
        this.content = content;
        this.isOpen = false;
    }
    
    open() {
        this.isOpen = true;
        console.log(`Modal "${this.title}" opened`);
    }
    
    close() {
        this.isOpen = false;
        console.log(`Modal "${this.title}" closed`);
    }
}

// Экспорт компонентов
export { Button, Modal };
