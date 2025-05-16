comments:
let
  # Render a single comment set as an HTML snippet
  renderComment = comment: ''
    <div class="comment">
      <div class="comment-header">
        <span class="comment-user">${comment.user}</span>
        <span class="comment-date">${comment.date}</span>
      </div>
      <div class="comment-body">
        ${comment.content}
      </div>
    </div>
  '';

in  # Main HTML for the comment section
''
<section id="comments">
  <h2>Comments</h2>
  ${builtins.concatStringsSep "\n" (builtins.map renderComment comments)}
</section>
''
