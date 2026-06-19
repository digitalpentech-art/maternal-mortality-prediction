export function showPage(pageId, element) {
    document.querySelectorAll('.page').forEach(p => p.classList.add('d-none'));
    const targetPage = document.getElementById(`page-${pageId}`);
    if (targetPage) targetPage.classList.remove('d-none');
    
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    if (element) element.classList.add('active');
}
