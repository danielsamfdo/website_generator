/* define the "selectedKeywords" variable in your document like so before
   including subpub.php:

	<script type="text/javascript">
		var selectedKeywords = "Health;Security";
	</script>
*/

// hint from http://hg.mozilla.org/users/axel_mozilla.com/dashboard/file/33880acb41c7/html/index.html#l12has
SimileAjax.jQuery(document).ready(function() {
	var fDone = function() {
		$('#pub-facets').hide(); // hide Exhibit facets
		$('.calmnotice').hide(); // hide notices ("flatten this list")

		if (typeof selectedKeywords !== 'undefined') {
			document.getElementById("keywords-facet").setAttribute("ex:selection", selectedKeywords);
		}

		window.exhibit = Exhibit.create();
		window.exhibit.configureFromDOM();
	};
	window.database = Exhibit.Database.create();
	window.database.loadDataLinks(fDone);
});
