var sidenav = document.querySelectorAll('.sidenav');
var sv_instances = M.Sidenav.init(sidenav);
var collapsible = document.querySelectorAll('.collapsible');
var col_instances = M.Collapsible.init(collapsible);
var select = document.querySelectorAll('select');
var select_instances = M.FormSelect.init(select);
var dropdown = document.querySelectorAll('.dropdown-trigger');
var drp_instances = M.Dropdown.init(dropdown, { 'coverTrigger': false });
var not_collapse = document.querySelectorAll('.not-collapse')
var modal = document.querySelectorAll('.modal');
var instances_modal = M.Modal.init(modal);
not_collapse.forEach(e => {
    e.addEventListener('click', function (ev) {
        ev.stopPropagation();
    })
});