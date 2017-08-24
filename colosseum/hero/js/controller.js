function BindEvents() {
    let showHeroes = () => {
        document.querySelectorAll('.hero-list li').forEach((ele, i) => {
            setTimeout(() => ele.classList.add('visible'), 50+(50*i));
        });
        
        document.querySelector('.hero-list').classList.remove('loading');
    }
    showHeroes();
    
    let loadCount = 0;
    document.querySelectorAll('.hero-list li img').forEach((ele, i) => {
        loadCount++;
        ele.addEventListener('load', (e) => {
            console.debug("Img loaded", loadCount);
            loadCount--;
            if(loadCount <= 0) { showHeroes() }
        });
    });
    
    setTimeout(() => {
        if(loadCount > 0)
            showHeroes(); // We don't care at this point, it's been too long.
    }, 2000);
}

// Listen to event for importing for the hero page template
function bindController() {
    document.body.addEventListener('template.hero-template', BindEvents);
}

export default {
    bind: bindController,
};
