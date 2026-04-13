<script setup>

</script>


<template>
  <div class="container mx-auto py-14 px-20">
    <div class="flex space-x-8 mt-4">
      <div class="w-full flex flex-col justify-start items-start space-y-8">
        <div class="w-full flex flex-col justify-start items-start p-8 rounded-lg">
          <div class="w-full mb-4 border-b-2 border-gray-200 pb-5">
            <p class="text-2xl leading-5 text-gray-800">Popular Events</p>
            <div class="mt-4 flex flex-row gap-3 transition-transform duration-500 ease-out pb-3">
              <RouterLink to="/" class="bg-gray-50 w-[27%] shadow-sm rounded-3xl overflow-hidden hover:scale-105 transition-scale duration-300 cursor-pointer">
                <img src="https://unsplash.it/600/300?image=1050" alt="Team Member 1" class="w-full h-48 object-cover">
                <div class="p-6">
                  <h2 class="text-xl font-semibold">Jane Smith</h2>
                  <time class="text-md text-gray-600">Mon, Apr 6 · 12:00 PM CEST</time>
                  <p class="text-sm text-gray-600">by user</p>
                </div>
              </RouterLink>

              <RouterLink to="/" class="bg-gray-50 w-[27%] shadow-sm rounded-3xl overflow-hidden hover:scale-105 transition-scale duration-300 cursor-pointer">
                <img src="https://unsplash.it/600/300?image=1060" alt="Team Member 2" class="w-full h-48 object-cover">
                <div class="p-6">
                  <h2 class="text-xl font-semibold">Jane Smith</h2>
                  <time class="text-md text-gray-600">Mon, Apr 6 · 12:00 PM CEST</time>
                  <p class="text-sm text-gray-600">by user</p>
                </div>
              </RouterLink>

              <RouterLink to="/" class="bg-gray-50 w-[27%] shadow-sm rounded-3xl overflow-hidden hover:scale-105 transition-scale duration-300 cursor-pointer">
                <img src="https://unsplash.it/600/300?image=1070" alt="Team Member 3" class="w-full h-48 object-cover">
                <div class="p-6">
                  <h2 class="text-xl font-semibold">Jane Smith</h2>
                  <time class="text-md text-gray-600">Mon, Apr 6 · 12:00 PM CEST</time>
                  <p class="text-sm text-gray-600">by user</p>
                </div>
              </RouterLink>
            </div>
          </div>
          <div class="w-full">
            <p class="text-2xl leading-5 text-gray-800">Explore Communities</p>
            <div class="mt-4 flex flex-row gap-3 transition-transform duration-500 ease-out">
              <RouterLink to="/" class="bg-gray-50 w-[27%] shadow-sm rounded-3xl overflow-hidden hover:scale-105 transition-scale duration-300 cursor-pointer">
                <img src="https://unsplash.it/600/300?image=1020" alt="Team Member 1" class="w-full h-48 object-cover">
                <div class="p-6">
                  <h2 class="text-xl font-semibold">Jane Smith</h2>
                  <time class="text-md text-gray-600">Mon, Apr 6 · 12:00 PM CEST</time>
                  <p class="text-sm text-gray-600">by user</p>
                </div>
              </RouterLink>

              <RouterLink to="/" class="bg-gray-50 w-[27%] shadow-sm rounded-3xl overflow-hidden hover:scale-105 transition-scale duration-300 cursor-pointer">
                <img src="https://unsplash.it/600/300?image=1010" alt="Team Member 2" class="w-full h-48 object-cover">
                <div class="p-6">
                  <h2 class="text-xl font-semibold">Jane Smith</h2>
                  <time class="text-md text-gray-600">Mon, Apr 6 · 12:00 PM CEST</time>
                  <p class="text-sm text-gray-600">by user</p>
                </div>
              </RouterLink>

              <RouterLink to="/" class="bg-gray-50 w-[27%] shadow-sm rounded-3xl overflow-hidden hover:scale-105 transition-scale duration-300 cursor-pointer">
                <img src="https://unsplash.it/600/300?image=1040" alt="Team Member 3" class="w-full h-48 object-cover">
                <div class="p-6">
                  <h2 class="text-xl font-semibold">Jane Smith</h2>
                  <time class="text-md text-gray-600">Mon, Apr 6 · 12:00 PM CEST</time>
                  <p class="text-sm text-gray-600">by user</p>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
      <div class="w-96 flex justify-between items-center p-8 flex-col border-l-2 border-gray-200">
        <h3 class="text-xl leading-5">Events This Week</h3>
        <div class="flex flex-col justify-start items-start mt-6 h-full w-full space-x-0 text-white">
          <RouterLink to="/" class="bg-gray-800 rounded-md p-6 mb-4 hover:scale-105 transition-scale duration-300 cursor-pointer">
            <h3 class="text-xl text-gray-300">Hiking Adventure</h3>
            <p class="mt-1 text-gray-400 text-sm">Mon, Apr 6 · 10:00 AM</p>
            <p class="mt-1 text-gray-400 text-sm">Location: Blue Mountain Park</p>
            <p class="mt-2 text-sm">
              Join us for a morning hike in the beautiful mountains nearby. Suitable for all skill levels. Don't forget to bring water and snacks.
            </p>
            <p class="text-sm text-gray-500 mt-2">Organized by: user</p>
          </RouterLink>

          <RouterLink to="/" class="bg-gray-800 rounded-md p-6 mb-4 hover:scale-105 transition-scale duration-300 cursor-pointer">
            <h3 class="text-xl text-gray-300">Book Club Meetup</h3>
            <p class="mt-1 text-gray-400 text-sm">Tue, Apr 7 · 6:00 PM</p>
            <p class="mt-1 text-gray-400 text-sm">Location: Downtown Library</p>
            <p class="mt-2 text-sm">
              Discuss this month's selected book with fellow readers over coffee. All book lovers are welcome!
            </p>
            <p class="text-gray-500 mt-2">Organized by: user</p>
          </RouterLink>

          <RouterLink to="/" class="bg-gray-800 rounded-md p-6 mb-4 hover:scale-105 transition-scale duration-300 cursor-pointer">
            <h3 class="text-xl text-gray-300">Cooking Workshop</h3>
            <p class="mt-1 text-gray-400 text-sm">Wed, Apr 8 · 5:00 PM</p>
            <p class="mt-1 text-gray-400 text-sm">Location: Culinary School Kitchen</p>
            <p class="mt-2 text-sm">
              Learn new recipes and cooking techniques from a professional chef. Ingredients are provided. Bring your appetite!
            </p>
            <p class="text-gray-500 mt-2">Organized by: user</p>
          </RouterLink>
        </div>

        <RouterLink to="/" class="text-center mt-6 py-5 hover:bg-gray-500 bg-gray-800 w-full text-base font-medium leading-4 text-gray-200 transform-color duration-300">View All</RouterLink>
      </div>
    </div>
  </div>
</template>
