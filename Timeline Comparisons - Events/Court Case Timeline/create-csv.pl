#!/usr/bin/env perl

# https://www.fairfaxcounty.gov/circuit/high-profile-cases

use Data::Dumper;

use Cache::FileCache;
use Text::CSV qw(csv);
use WWW::Mechanize::Cached;

my $cacheobj = new Cache::FileCache
  ({
    namespace => 'worldie',
    default_expires_in => "1 week",
    cache_root => "/tmp/worldie",
   });

my $mech = WWW::Mechanize::Cached->new
  (
   cache => $cacheobj,
   timeout => 15,
  );

$mech->get('https://www.fairfaxcounty.gov/circuit/high-profile-cases');
my $c = $mech->content;

$c =~ s/.*?John C. Depp, II v. Amber Laura Heard//sg;
$c =~ s/Elon Wilson.*//sg;

my @results = (['CASE NUMBER: CL-2019-2911 - JOHN C. DEPP, II V. AMBER LAURA HEARD',undef,undef],['Date','Documents','PDF']);
if ($c =~ /<tbody>(.*?)<\/tbody>/s) {
  my $table = $1;
  my @data = $table =~ /<tr>\s*<td>(.*?)<\/td>\s*<td>(.*?)<\/td>\s*<td>(.*?)<\/td>\s*<\/tr>\s*?/sg;
  while (@data) {
    my $a = shift @data;
    my $b = shift @data;
    my $c = shift @data;
    push @results, [$a,$b,$c];
  }
}
csv(in => \@results, out => "output.csv", sep_char=> ",")
